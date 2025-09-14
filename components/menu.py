"""Menu component - handles menu display and dish selection"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from constants.texts import texts
from constants.variables import (
    get_current_menu, find_dish_by_name, current_portions_count, MAX_PORTIONS, WEEKLY_DISH
)

def get_weekly_dish_text():
    """Generate beautiful weekly dish display using new format"""
    dish = WEEKLY_DISH
    
    # Format ingredients list
    ingredients_list = "\n".join([f"• {ingredient}" for ingredient in dish['ingredients']])
    
    # Format allergens list  
    allergens_list = "\n".join([f"• {allergen}" for allergen in dish['allergens']])
    
    # Format nutrition info
    nutrition_list = "\n".join([f"• {key.title()}: {value}" for key, value in dish['nutrition'].items()])
    
    return (
        f"{texts.get('WEEKLY_DISH_TITLE', dish_name=dish['name'])}\n\n"
        f"{texts.get('DELIVERY_DAY_TITLE', day=dish['delivery_day'])}\n\n"
        f"{texts.get('PRICE_TITLE', price=dish['price'])}\n\n"
        f"{texts.INGREDIENTS_TITLE}\n{ingredients_list}\n\n"
        f"{texts.ALLERGENS_TITLE}\n{allergens_list}\n\n"
        f"{texts.NUTRITION_TITLE}\n{nutrition_list}\n\n"
        f"{texts.EXTRA_INFO_TITLE}\n{dish['extra_info']}\n\n"
        f"📍 **Location:** {dish['location']}\n"
        f"⏰ **Delivery Time:** {dish['delivery_time']}"
    )

def get_details_text():
    """Legacy function - kept for compatibility"""
    return get_weekly_dish_text()

async def display_menu_of_week(update: Update, context: CallbackContext):
    """Display the weekly featured dish directly (no selection needed since there's only one dish)"""
    if current_portions_count >= MAX_PORTIONS:
        await update.callback_query.answer(texts.COMPLETELY_FULL_MESSAGE, show_alert=True)
        return

    # Store the weekly dish in user context
    context.user_data["selected_dish"] = WEEKLY_DISH["display_name"].lower().replace(" ", "_")
    context.user_data["selected_days"] = [WEEKLY_DISH["delivery_day"]]  # Pre-select the fixed delivery day
    
    # Create the order button (no day selection needed since it's fixed)
    keyboard = [
        [InlineKeyboardButton(texts.ORDER_BUTTON_TEXT, callback_data="proceed_to_address")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        get_weekly_dish_text(), 
        parse_mode="Markdown", 
        reply_markup=reply_markup
    )

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
