"""Ordering component - handles the complete ordering process"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from urllib.parse import quote, unquote
import threading
import asyncio
from datetime import datetime
from constants.texts import texts
from constants.variables import (
    ADMIN_TELEGRAM_ID, CONTACT_ADMIN, ORDERS_LOG_FILE, PORTION_COUNT_FILE,
    is_valid_quantity, is_within_portion_limit, get_remaining_portions,
    current_portions_count, MAX_PORTIONS, QUALITY_CHECK_DELAY,
    get_available_portion_options, is_fully_reserved
)

def increment_portions_count(quantity):
    """Add the ordered quantity to the total count"""
    global current_portions_count
    current_portions_count += quantity
    with open(PORTION_COUNT_FILE, 'w') as f:
        f.write(str(current_portions_count))

async def toggle_day(update: Update, context: CallbackContext):
    """Toggle day selection"""
    query = update.callback_query
    selected_day = query.data.split("_")[1]

    if "selected_days" not in context.user_data:
        context.user_data["selected_days"] = []

    if selected_day in context.user_data["selected_days"]:
        context.user_data["selected_days"].remove(selected_day)
    else:
        context.user_data["selected_days"].append(selected_day)

    keyboard = [
        [InlineKeyboardButton(
            "☑️ Saturday" if "Saturday" in context.user_data["selected_days"] else "⬜ Saturday",
            callback_data="toggle_Saturday")],
        [InlineKeyboardButton("✅ Confirm", callback_data="confirm_day")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_reply_markup(reply_markup=reply_markup)

async def confirm_day(update: Update, context: CallbackContext):
    """Confirm the selected delivery days"""
    query = update.callback_query
    selected_days = context.user_data.get("selected_days", [])

    if not selected_days:
        await query.answer(texts.SELECT_AT_LEAST_ONE_DAY, show_alert=True)
        return

    days_text = ", ".join(selected_days)
    context.user_data["final_selected_days"] = days_text

    address_keyboard = [
        [InlineKeyboardButton("📍 Loreto Square", callback_data="address_Loreto")],
        [InlineKeyboardButton("📍 Politecnico di Milano - Piola", callback_data="address_Piola")]
    ]
    address_markup = InlineKeyboardMarkup(address_keyboard)

    await query.edit_message_text(
        texts.get("DELIVERY_SELECTED", days=days_text),
        parse_mode="Markdown",
        reply_markup=address_markup
    )

async def show_portion_selection(update: Update, context: CallbackContext):
    """Show portion selection buttons with dynamic availability based on remaining capacity"""
    query = update.callback_query
    
    # Check if delivery is fully reserved
    if is_fully_reserved():
        await query.answer()
        await query.edit_message_text(
            texts.FULLY_RESERVED_MESSAGE,
            parse_mode="Markdown"
        )
        return
    
    # Get available portion options based on remaining capacity
    available_options = get_available_portion_options()
    remaining = get_remaining_portions()
    
    # Create dynamic portion buttons based on availability
    portion_buttons = {
        1: texts.PORTION_1_BUTTON,
        2: texts.PORTION_2_BUTTON,
        3: texts.PORTION_3_BUTTON,
        4: texts.PORTION_4_BUTTON
    }
    
    keyboard = []
    
    # Add available portion buttons
    for portion_num in available_options:
        if portion_num in portion_buttons:
            keyboard.append([InlineKeyboardButton(
                portion_buttons[portion_num], 
                callback_data=f"portion_{portion_num}"
            )])
    
    # Always add contact admin button for more portions
    keyboard.append([InlineKeyboardButton(
        texts.CONTACT_ADMIN_MORE_BUTTON, 
        url="https://t.me/mrlibro"
    )])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Create dynamic title with remaining portions info
    title_with_info = (
        f"{texts.PORTION_SELECTION_TITLE}\n\n"
        f"📊 **Available portions: {remaining}/{MAX_PORTIONS}**"
    )
    
    await query.answer()
    await query.edit_message_text(
        title_with_info,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def select_address(update: Update, context: CallbackContext):
    """Handle address selection"""
    query = update.callback_query
    selected_address = query.data.split("_")[1]
    context.user_data["selected_address"] = selected_address

    callback_data = f"add_{quote(context.user_data['selected_dish'])}"
    keyboard = [[InlineKeyboardButton(texts.ADD_TO_BASKET_BUTTON, callback_data=callback_data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.answer()
    await query.edit_message_text(
        texts.get("ADDRESS_SELECTED", 
                 address=selected_address, 
                 days=context.user_data.get('final_selected_days', 'Not specified')),
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def add_to_basket(update: Update, context: CallbackContext):
    """Start the quantity selection process"""
    if current_portions_count >= MAX_PORTIONS:
        await update.callback_query.answer(texts.COMPLETELY_FULL_MESSAGE, show_alert=True)
        return

    query = update.callback_query
    dish_name = unquote(query.data.split("_", 1)[1])
    selected_days = context.user_data.get("final_selected_days", "Not specified")
    selected_address = context.user_data.get("selected_address", "Not specified")

    await query.answer()
    await query.edit_message_text(
        f"{texts.DISH_NAME_TEXT} {dish_name}\n"
        f"{texts.DELIVERY_DATE_TEXT} {selected_days}\n"
        f"📍 *Delivery Address:* {selected_address}\n\n"
        "🔢 *How many portions would you like to order?* (1-4)\n"
        f"⚠️ If you need more than 4 portions, please contact the admin: [Contact Admin]({CONTACT_ADMIN})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

    context.user_data["pending_order"] = {
        "dish": dish_name,
        "days": selected_days,
        "address": selected_address
    }
    context.user_data["awaiting_quantity"] = True

async def receive_quantity(update: Update, context: CallbackContext):
    """Process the quantity input and finalize the order"""
    if "awaiting_quantity" not in context.user_data:
        return

    user_input = update.message.text.strip()

    if not user_input.isdigit():
        await update.message.reply_text(f"{texts.INVALID_QUANTITY_MESSAGE} Try again:")
        return

    quantity = int(user_input)

    if not is_within_portion_limit(quantity):
        remaining = get_remaining_portions()
        await update.message.reply_text(
            texts.get("PORTIONS_LIMIT_ERROR", remaining=remaining),
            parse_mode="Markdown"
        )
        return

    if not is_valid_quantity(quantity):
        await update.message.reply_text(
            texts.QUANTITY_RANGE_ERROR,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

    # Process the order
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "NoUsername"
    order_details = context.user_data["pending_order"]
    order_details["quantity"] = quantity

    order_message = (
        f"{texts.NEW_ORDER_RECEIVED}\n\n"
        f"{texts.USER_TEXT} @{username} (ID: {user_id})\n"
        f"{texts.DISH_NAME_TEXT} {order_details['dish']}\n"
        f"{texts.PORTIONS_TEXT} {quantity}\n"
        f"{texts.DELIVERY_DATE_TEXT} {order_details['days']}\n"
        f"📍 *Delivery Address:* {order_details['address']}\n"
    )
    
    increment_portions_count(quantity)

    await context.bot.send_message(chat_id=ADMIN_TELEGRAM_ID, text=order_message, parse_mode="Markdown")

    with open(ORDERS_LOG_FILE, "a") as file:
        file.write(
            f"{user_id} | @{username} | {order_details['dish']} | "
            f"{quantity} portions | {order_details['days']} | "
            f"{order_details['address']}\n"
        )

    await update.message.reply_text(
        texts.get("PORTIONS_ADDED_SUCCESS", quantity=quantity, dish=order_details['dish']) + "\n"
        f"{texts.DELIVERY_DATE_TEXT} {order_details['days']}\n"
        f"📍 *Delivery Address:* {order_details['address']}\n\n"
        f"{texts.PRE_RESERVATION_MESSAGE}",
        parse_mode="Markdown"
    )

    # Schedule quality check
    def send_check():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        from components.quality import send_quality_check
        loop.run_until_complete(send_quality_check(context, user_id, order_details))
        loop.close()

    threading.Timer(QUALITY_CHECK_DELAY, send_check).start()

    context.user_data.clear()
    await update.message.reply_text(texts.PLACE_ANOTHER_ORDER)

async def handle_portion_selection(update: Update, context: CallbackContext):
    """Handle portion selection from buttons and complete the order"""
    if current_portions_count >= MAX_PORTIONS:
        await update.callback_query.answer(texts.COMPLETELY_FULL_MESSAGE, show_alert=True)
        return

    query = update.callback_query
    portion_str = query.data.split("_")[1]  # Extract portion number
    quantity = int(portion_str)
    
    # Validate quantity
    if not is_within_portion_limit(quantity):
        remaining = get_remaining_portions()
        await query.answer(
            texts.get("PORTIONS_LIMIT_ERROR", remaining=remaining),
            show_alert=True
        )
        return

    if not is_valid_quantity(quantity):
        await query.answer(texts.QUANTITY_RANGE_ERROR, show_alert=True)
        return

    # Process the order immediately (streamlined flow)
    user_id = query.from_user.id
    username = query.from_user.username or "NoUsername"
    
    # Get dish info from context (set in menu display)
    from constants.variables import WEEKLY_DISH
    dish_name = WEEKLY_DISH["display_name"]
    delivery_day = WEEKLY_DISH["delivery_day"]
    
    # For now, we'll use a default address since we're skipping address selection
    # This can be configured or made optional later
    default_address = "Loreto Square"  # Can be made configurable
    
    order_details = {
        "dish": dish_name,
        "quantity": quantity,
        "days": delivery_day,
        "address": default_address
    }

    # Send order to admin
    order_message = (
        f"{texts.NEW_ORDER_RECEIVED}\n\n"
        f"{texts.USER_TEXT} @{username} (ID: {user_id})\n"
        f"{texts.DISH_NAME_TEXT} {dish_name}\n"
        f"{texts.PORTIONS_TEXT} {quantity}\n"
        f"{texts.DELIVERY_DATE_TEXT} {delivery_day}\n"
        f"📍 *Delivery Address:* {default_address}\n"
    )
    
    increment_portions_count(quantity)

    await context.bot.send_message(chat_id=ADMIN_TELEGRAM_ID, text=order_message, parse_mode="Markdown")

    # Log the order
    with open(ORDERS_LOG_FILE, "a") as file:
        file.write(
            f"{user_id} | @{username} | {dish_name} | "
            f"{quantity} portions | {delivery_day} | "
            f"{default_address}\n"
        )

    # Confirm order to user
    await query.answer("✅ Order placed successfully!")
    await query.edit_message_text(
        f"{texts.ORDER_CONFIRMATION_TITLE}\n\n"
        f"{texts.DISH_NAME_TEXT} {dish_name}\n"
        f"{texts.QUANTITY_TEXT} {quantity}\n"
        f"{texts.DELIVERY_DATE_TEXT} {delivery_day}\n"
        f"📍 *Delivery Address:* {default_address}\n\n"
        f"{texts.PRE_RESERVATION_MESSAGE}",
        parse_mode="Markdown"
    )

    # Schedule quality check
    def send_check():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        from components.quality import send_quality_check
        loop.run_until_complete(send_quality_check(context, user_id, order_details))
        loop.close()

    threading.Timer(QUALITY_CHECK_DELAY, send_check).start()

    # Clear user data
    context.user_data.clear()
    
    # Send follow-up message
    await context.bot.send_message(
        chat_id=user_id,
        text=texts.PLACE_ANOTHER_ORDER
    )
