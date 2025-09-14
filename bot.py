from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from urllib.parse import quote, unquote
import logging
import threading
import asyncio
from datetime import datetime, timedelta

# Import constants and variables
from constants.texts import texts
from constants.variables import (
    TOKEN, ADMIN_TELEGRAM_ID, CONTACT_ADMIN,
    MAX_PORTIONS, ORDERS_LOG_FILE, PORTION_COUNT_FILE,
    MIN_QUANTITY, MAX_QUANTITY, QUALITY_CHECK_DELAY,
    MENU_OF_WEEK, current_portions_count,
    get_current_menu, is_within_portion_limit, get_remaining_portions,
    is_valid_quantity, find_dish_by_name, validate_configuration
)

# Use the menu from constants
menu_of_week = get_current_menu()

def get_details_text():
    """Generate details text using constants and current menu data"""
    current_menu = get_current_menu()
    if not current_menu:
        return texts.NO_MENU_AVAILABLE
    
    dish = current_menu[0]  # Get first dish
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

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def welcome_message(update: Update, context: CallbackContext):
    intro_text = (
        f"{texts.WELCOME_TITLE}\n\n"
        f"{texts.WELCOME_GREETING} \n"
        f"{texts.WELCOME_BOT_INTRO}\n\n"
        
        f"{texts.WHAT_IS_LIBROCHEF_TITLE}\n"
        f"{texts.WHAT_IS_LIBROCHEF_DESC}\n\n"

        f"{texts.HOW_CAN_I_HELP_TITLE}\n"
        f"{texts.HOW_CAN_I_HELP_DESC}\n\n"

        f"{texts.LETS_GET_STARTED}"
    )

    # Create a button that triggers the /menuOfWeek command
    keyboard = [
        [InlineKeyboardButton(texts.SHOW_MENU_BUTTON, callback_data='menu_of_week')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the welcome message with the button
    await update.effective_message.reply_text(intro_text, parse_mode="Markdown", reply_markup=reply_markup)

def check_portions_limit(quantity):
    """Check if adding this quantity would exceed the limit"""
    return not is_within_portion_limit(quantity)

def increment_portions_count(quantity):
    """Add the ordered quantity to the total count"""
    global current_portions_count
    current_portions_count += quantity
    # Save to file for persistence
    with open(PORTION_COUNT_FILE, 'w') as f:
        f.write(str(current_portions_count))

def load_portions_count():
    """Load portion count from file (for bot restarts)"""
    global current_portions_count
    try:
        with open(PORTION_COUNT_FILE, 'r') as f:
            current_portions_count = int(f.read())
    except (FileNotFoundError, ValueError):
        current_portions_count = 0

async def display_menu_of_week(update: Update, context: CallbackContext):
    # Correct usage of menu_of_week, ensuring it's a list of dishes

    if current_portions_count >= MAX_PORTIONS:
        await update.callback_query.answer(
            texts.COMPLETELY_FULL_MESSAGE,
            show_alert=True
        )
        return

    current_menu = get_current_menu()
    keyboard = [
        [InlineKeyboardButton(dish['name'], callback_data=dish['name']) for dish in current_menu]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the menu to the user
    await update.callback_query.message.reply_text(texts.SELECT_DISH_PROMPT,
                                                   reply_markup=reply_markup)

    # Answer the callback query (to remove the "loading" state)
    await update.callback_query.answer()

async def toggle_day(update: Update, context: CallbackContext):
    query = update.callback_query
    selected_day = query.data.split("_")[1]  # Get "Saturday" or "Sunday"

    if "selected_days" not in context.user_data:
        context.user_data["selected_days"] = []

    if selected_day in context.user_data["selected_days"]:
        context.user_data["selected_days"].remove(selected_day)  # Unselect
    else:
        context.user_data["selected_days"].append(selected_day)  # Select

    # Update buttons
    keyboard = [
        [
            InlineKeyboardButton("☑️ Saturday" if "Saturday" in context.user_data["selected_days"] else "⬜ Saturday",
                                 callback_data="toggle_Saturday"),
        ],
        [InlineKeyboardButton("✅ Confirm", callback_data="confirm_day")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def select_address(update: Update, context: CallbackContext):
    query = update.callback_query
    selected_address = query.data.split("_")[1]  # e.g., 'Loreto' or 'Duomo'

    # Store in context
    context.user_data["selected_address"] = selected_address

    # Create "Add to Basket" button
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


async def confirm_day(update: Update, context: CallbackContext):
    query = update.callback_query

    # Retrieve selected days
    selected_days = context.user_data.get("selected_days", [])

    if not selected_days:
        await query.answer(texts.SELECT_AT_LEAST_ONE_DAY, show_alert=True)
        return

    days_text = ", ".join(selected_days)

    # Store selected days in context for the next step
    context.user_data["final_selected_days"] = days_text

    # Address selection buttons
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


async def show_dish_details(update: Update, context: CallbackContext):
    query = update.callback_query
    dish_name = query.data  # Get the selected dish name



    dish = find_dish_by_name(dish_name)
    if dish:
        # Save selected dish in user context
        context.user_data["selected_dish"] = dish_name
        context.user_data["selected_days"] = []  # Empty list to store selected days

        # Create toggle buttons for Saturday
        keyboard = [
            [
                InlineKeyboardButton(
                    "☑️ Saturday" if "Saturday" in context.user_data["selected_days"] else "⬜ Saturday",
                    callback_data="toggle_Saturday")
            ],
            [InlineKeyboardButton("✅ Confirm", callback_data="confirm_day")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.answer()
        await query.edit_message_text(get_details_text(), parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await query.answer(texts.DISH_NOT_FOUND)

async def add_to_basket(update: Update, context: CallbackContext):

    # Check availability before proceeding
    if current_portions_count >= MAX_PORTIONS:
        await update.callback_query.answer(
            texts.COMPLETELY_FULL_MESSAGE,
            show_alert=True
        )
        return

    query = update.callback_query
    dish_name = unquote(query.data.split("_", 1)[1])

    # Retrieve selected days and address
    selected_days = context.user_data.get("final_selected_days", "Not specified")
    selected_address = context.user_data.get("selected_address", "Not specified")

    # Ask for portions
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

    # Save dish name and selected days in context
    context.user_data["pending_order"] = {
        "dish": dish_name,
        "days": selected_days,
        "address": selected_address
    }
    context.user_data["awaiting_quantity"] = True

# ADMIN_TELEGRAM_ID is now imported from constants.variables


async def receive_quantity(update: Update, context: CallbackContext):
    if "awaiting_quantity" not in context.user_data:
        return  # Ignore messages if not expecting input

    user_input = update.message.text.strip()

    if not user_input.isdigit():
        await update.message.reply_text(f"{texts.INVALID_QUANTITY_MESSAGE} Try again:")
        return

    quantity = int(user_input)

    # Check if this order would exceed the limit
    if check_portions_limit(quantity):
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

    # Save the order
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "NoUsername"
    order_details = context.user_data["pending_order"]
    order_details["quantity"] = quantity  # Add quantity to order details

    # Format the order message
    order_message = (
        f"{texts.NEW_ORDER_RECEIVED}\n\n"
        f"{texts.USER_TEXT} @{username} (ID: {user_id})\n"
        f"{texts.DISH_NAME_TEXT} {order_details['dish']}\n"
        f"{texts.PORTIONS_TEXT} {quantity}\n"
        f"{texts.DELIVERY_DATE_TEXT} {order_details['days']}\n"
        f"📍 *Delivery Address:* {order_details['address']}\n"
    )
    # After successful order processing:
    increment_portions_count(quantity)

    # Send order details to admin
    await context.bot.send_message(chat_id=ADMIN_TELEGRAM_ID, text=order_message, parse_mode="Markdown")

    # Save order details in a text file
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

    # Schedule quality check for 1 minute later
    def send_check():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_quality_check(context, user_id, order_details))
        loop.close()

    threading.Timer(QUALITY_CHECK_DELAY, send_check).start()

    # End session and force user to restart
    context.user_data.clear()
    await update.message.reply_text(texts.PLACE_ANOTHER_ORDER)

async def error_handler(update: Update, context: CallbackContext):
    """Handle errors and notify user."""
    try:
        await update.message.reply_text(
            texts.get("BOT_ERROR_MESSAGE", contact_admin=CONTACT_ADMIN),
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Error sending message: {e}")

async def send_quality_check(context: CallbackContext, user_id: int, order_details: dict):
    try:
        # Create initial quality check buttons
        keyboard = [
            [InlineKeyboardButton("👍 Good", callback_data=f"quality_good_{user_id}")],
            [InlineKeyboardButton("👎 Needs Improvement", callback_data=f"quality_bad_{user_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            f"{texts.QUALITY_CHECK_TITLE}\n\n"
            f"{texts.DISH_NAME_TEXT} {order_details['dish']}\n"
            f"{texts.PORTIONS_TEXT} {order_details['quantity']}\n\n"
            f"{texts.QUALITY_RATING_PROMPT}"
        )

        # Use the context's bot instance directly
        await context.bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Error sending quality check: {e}")

async def handle_quality_feedback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    quality = data[1]  # 'good' or 'bad'
    user_id = data[2]

    # Store the rating in user_data
    context.user_data["quality_rating"] = quality
    context.user_data["awaiting_feedback_text"] = True

    # Ask for additional feedback
    rating_type = texts.POSITIVE_RATING if quality == 'good' else texts.CONSTRUCTIVE_RATING
    await query.edit_message_text(
        f"Thank you for your {rating_type} rating!\n\n"
        f"{texts.ADDITIONAL_COMMENTS_PROMPT}",
        parse_mode="Markdown"
    )

async def receive_feedback_text(update: Update, context: CallbackContext):
    # Only handle if we're expecting feedback text
    if not context.user_data.get("awaiting_feedback_text"):
        return

    if "quality_rating" not in context.user_data:
        return

    feedback_text = update.message.text
    user_id = update.message.from_user.id
    quality = context.user_data["quality_rating"]
    username = update.message.from_user.username or "NoUsername"

    # Notify admin
    feedback_message = (
        f"{texts.QUALITY_FEEDBACK_RECEIVED}\n\n"
        f"{texts.USER_TEXT} @{username} (ID: {user_id})\n"
        f"{texts.RATING_TEXT} {'Good' if quality == 'good' else 'Needs Improvement'}\n"
        f"{texts.FEEDBACK_TEXT} {feedback_text}\n"
        f"{texts.TIME_TEXT} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_TELEGRAM_ID,
            text=feedback_message,
            parse_mode="Markdown"
        )
        await update.message.reply_text(
            texts.THANK_YOU_FEEDBACK
        )
    except Exception as e:
        logging.error(f"Error sending feedback: {e}")
        await update.message.reply_text(
            texts.FEEDBACK_ERROR
        )

    # Clean up
    context.user_data.clear()

async def skip_feedback(update: Update, context: CallbackContext):
    if not context.user_data.get("awaiting_feedback_text"):
        return

    user_id = update.message.from_user.id
    quality = context.user_data["quality_rating"]
    username = update.message.from_user.username or "NoUsername"

    # Notify admin
    feedback_message = (
        f"{texts.QUALITY_FEEDBACK_RECEIVED}\n\n"
        f"{texts.USER_TEXT} @{username} (ID: {user_id})\n"
        f"{texts.RATING_TEXT} {'Good' if quality == 'good' else 'Needs Improvement'}\n"
        f"{texts.FEEDBACK_TEXT} {texts.NO_ADDITIONAL_COMMENTS}\n"
        f"{texts.TIME_TEXT} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_TELEGRAM_ID,
            text=feedback_message,
            parse_mode="Markdown"
        )
        await update.message.reply_text(
            texts.THANK_YOU_RATING
        )
    except Exception as e:
        logging.error(f"Error sending feedback: {e}")
        await update.message.reply_text(
            texts.FEEDBACK_PROCESS_ERROR
        )

    # Clean up
    context.user_data.clear()

def is_expecting_quantity(context: CallbackContext) -> bool:
    return context.user_data.get("awaiting_quantity", False)

def is_expecting_feedback(context: CallbackContext) -> bool:
    return context.user_data.get("awaiting_feedback_text", False)



def main():
    # Validate configuration on startup
    config_errors = validate_configuration()
    if config_errors:
        print("❌ Configuration errors found:")
        for error in config_errors:
            print(f"  - {error}")
        print("Please fix these issues before starting the bot.")
        return
    
    print("✅ Configuration validated successfully!")
    load_portions_count()
    try:
        app = Application.builder().token(TOKEN).build()

        # Add command handlers
        app.add_handler(CommandHandler("start", welcome_message))
        app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text("Available commands: /start /help")))
        app.add_handler(CommandHandler("skip", skip_feedback))

        # Callback handlers
        app.add_handler(CallbackQueryHandler(display_menu_of_week, pattern='^menu_of_week$'))
        app.add_handler(CallbackQueryHandler(toggle_day, pattern=r"^toggle_.*"))
        app.add_handler(CallbackQueryHandler(confirm_day, pattern="confirm_day"))
        app.add_handler(CallbackQueryHandler(show_dish_details, pattern=r'^kir$'))
        app.add_handler(CallbackQueryHandler(select_address, pattern=r"^address_.*"))
        app.add_handler(CallbackQueryHandler(add_to_basket, pattern=r'^add_.*'))
        app.add_handler(CallbackQueryHandler(handle_quality_feedback, pattern=r'^quality_(good|bad)_\d+$'))

        # Message handlers
        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Regex(r'^\d+$') & filters.ChatType.PRIVATE,
            receive_quantity
        ))
        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
            receive_feedback_text
        ))

        # Register the error handler
        app.add_error_handler(error_handler)

        print("Bot is running...")
        app.run_polling()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"Bot failed to start. Please check the logs for errors: {e}")


if __name__ == "__main__":
    main()