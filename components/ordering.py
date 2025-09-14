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
    current_portions_count, MAX_PORTIONS, QUALITY_CHECK_DELAY
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
