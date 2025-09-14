"""Menu component - handles menu display and dish selection"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from constants.texts import texts
from constants.variables import (
    get_current_menu, find_dish_by_name, current_portions_count, MAX_PORTIONS
)

def get_details_text():
    """Generate details text using constants and current menu data"""
    current_menu = get_current_menu()
    if not current_menu:
        return texts.NO_MENU_AVAILABLE
    
    dish = current_menu[0]
    return (
        f"{texts.MENU_PACK_PREFIX} {dish['name']}*\n\n"
        f"{texts.CUTLET_COUNT_TEXT}\n"
        f"{texts.PRICE_TEXT}{dish['price']}\n"
        f"{texts.MEAT_TEXT}\n"
        f"{texts.EGG_TEXT}\n"
        f"{texts.POTATO_TEXT}\n"
        f"{texts.ONION_TEXT}\n"
        f"{texts.GARLIC_TEXT}\n"
        f"{texts.SANDWICH_INSIDE_TEXT}\n"
        f"{texts.SERVED_WITH_TEXT}\n"
        f"{texts.ALLERGEN_INFO_TEXT}\n\n"
        f"{texts.DELIVERY_TIME_TEXT} {dish['time_of_delivery']}\n"
        f"{texts.LOCATION_TEXT} {dish['location']}\n\n"
        f"{texts.MEAT_QUALITY_TEXT}\n\n"
        f"{texts.SELECT_DELIVERY_DAY_TEXT}"
    )

async def display_menu_of_week(update: Update, context: CallbackContext):
    """Display the weekly menu"""
    if current_portions_count >= MAX_PORTIONS:
        await update.callback_query.answer(texts.COMPLETELY_FULL_MESSAGE, show_alert=True)
        return

    current_menu = get_current_menu()
    keyboard = [
        [InlineKeyboardButton(dish['name'], callback_data=dish['name']) for dish in current_menu]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(texts.SELECT_DISH_PROMPT, reply_markup=reply_markup)
    await update.callback_query.answer()

async def show_dish_details(update: Update, context: CallbackContext):
    """Show detailed information about a selected dish"""
    query = update.callback_query
    dish_name = query.data

    dish = find_dish_by_name(dish_name)
    if dish:
        context.user_data["selected_dish"] = dish_name
        context.user_data["selected_days"] = []

        keyboard = [
            [InlineKeyboardButton(
                "☑️ Saturday" if "Saturday" in context.user_data["selected_days"] else "⬜ Saturday",
                callback_data="toggle_Saturday")],
            [InlineKeyboardButton("✅ Confirm", callback_data="confirm_day")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.answer()
        await query.edit_message_text(get_details_text(), parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await query.answer(texts.DISH_NOT_FOUND)
