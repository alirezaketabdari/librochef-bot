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
    import constants.variables as vars_module
    vars_module.current_portions_count += quantity
    with open(PORTION_COUNT_FILE, 'w', encoding='utf-8') as f:
        f.write(str(vars_module.current_portions_count))

# toggle_day removed - not needed in streamlined flow

# confirm_day removed - not needed in streamlined flow

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

# select_address removed - not needed in streamlined flow

# add_to_basket removed - not needed in streamlined flow

# receive_quantity removed - not needed in streamlined flow

async def handle_portion_selection(update: Update, context: CallbackContext):
    """Handle portion selection from buttons and complete the order"""
    query = update.callback_query
    portion_str = query.data.split("_")[1]  # Extract portion number
    quantity = int(portion_str)
    
    # CRITICAL: Check if adding this quantity would exceed the limit
    if not is_within_portion_limit(quantity):
        remaining = get_remaining_portions()
        if remaining <= 0:
            await query.answer(texts.COMPLETELY_FULL_MESSAGE, show_alert=True)
        else:
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
