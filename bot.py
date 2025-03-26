from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

# Replace this with your bot token from BotFather 
TOKEN = "7803608326:AAGGVhBNpqFS9-ZPkOW35mh8nRFhJaYwnDY"


# Send automatic introduction when the user first interacts with the bot
async def welcome_message(update: Update, context: CallbackContext):
    intro_text = (
        "🍽️ *Welcome to the LibroChef Bot!* 🍽️\n\n"
        "Hello, my friend! 👋\n\n"
        "I am *LibroChef Bot*, your gateway to a world of flavors and culinary mastery! 🍲🔥\n"
        "*LibroChef* is a culinary studio dedicated to *learning, teaching, and refining* the art of cooking. "
        "We explore everything from *traditional local dishes* to *modern gastronomy*, pushing our limits in "
        "*large-scale catering, advanced cooking techniques, and recipe development.*\n\n"
        "This bot is here for one essential task: *managing deliveries and registering your name* for our exclusive culinary experiences. 🍕📦\n\n"
        "Let’s get started! 🚀\n\n"
        "I'm here to help you with our weekly menu.\n"
    )

    # Create a button that triggers the /menuOfWeek command
    keyboard = [
        [InlineKeyboardButton("Show Menu of the Week", callback_data='menu_of_week')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the welcome message with the button
    await update.message.reply_text(intro_text, parse_mode="Markdown", reply_markup=reply_markup)


# Callback function to show details of the selected dish
async def show_dish_details(update: Update, context: CallbackContext):
    query = update.callback_query
    dish_name = query.data  # Get the selected dish name

    menu_of_week = [
        {"name": "Spaghetti Bolognese", "ingredients": "Pasta, Beef, Tomatoes, Garlic, Onion", "price": 12, "location": "Milan", "time_of_delivery": "12:00-14:00", "description": "Classic Italian pasta with rich Bolognese sauce."},
        {"name": "Margherita Pizza", "ingredients": "Tomato, Mozzarella, Basil, Olive Oil", "price": 10, "location": "Milan", "time_of_delivery": "12:00-14:00", "description": "Traditional pizza with mozzarella and fresh basil."},
    ]

    # Find the selected dish in the menu
    dish = next((d for d in menu_of_week if d['name'] == dish_name), None)

    if dish:
        details_text = (
            f"🍽 *{dish['name']}*\n\n"
            f"📌 *Ingredients:* {dish['ingredients']}\n"
            f"💰 *Price:* €{dish['price']}\n"
            f"⏰ *Delivery Time:* {dish['time_of_delivery']}\n"
            f"📍 *Location:* {dish['location']}\n\n"
            f"{dish['description']}\n"
        )

        await query.answer()
        await query.message.reply_text(details_text, parse_mode="Markdown")

        # "Add to Basket" button
        keyboard = [[InlineKeyboardButton("🛒 Add to Basket", callback_data=f"add_{dish_name}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text("Would you like to add this dish to your basket?", reply_markup=reply_markup)
    else:
        await query.answer("Dish not found.")

# Command to display menu
async def display_menu_of_week(update: Update, context: CallbackContext):
    # Correct usage of menu_of_week, ensuring it's a list of dishes
    menu_of_week = [
        {"name": "Spaghetti Bolognese", "image": "https://example.com/spaghetti.jpg", "ingredients": "Pasta, Beef, Tomatoes, Garlic, Onion", "price": 12, "location": "Milan", "time_of_delivery": "12:00-14:00", "description": "Classic Italian pasta with rich Bolognese sauce."},
        {"name": "Margherita Pizza", "image": "https://example.com/pizza.jpg", "ingredients": "Tomato, Mozzarella, Basil, Olive Oil", "price": 10, "location": "Milan", "time_of_delivery": "12:00-14:00", "description": "Traditional pizza with mozzarella and fresh basil."},
    ]

    keyboard = [
        [InlineKeyboardButton(dish['name'], callback_data=dish['name']) for dish in menu_of_week]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the menu to the user
    await update.callback_query.message.reply_text("Please select a dish from the menu of the week:", reply_markup=reply_markup)

    # Answer the callback query (to remove the "loading" state)
    await update.callback_query.answer()

# To track the basket (user orders)
user_baskets = {}

# Add dish to the basket
async def add_to_basket(update: Update, context: CallbackContext):
    query = update.callback_query
    dish_name = query.data.split("_", 1)[1]

    # Ask the user for the number of portions
    await query.answer()
    await query.message.reply_text(f"How many portions of *{dish_name}* would you like to order?", parse_mode="Markdown")

    # Store in the context for further processing
    user_baskets[query.from_user.id] = {
        "dish": dish_name,
        "portions": 0,
        "delivery_time": None
    }

# Receive number of portions
async def set_portions(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    dish_name = user_baskets[user_id]['dish']
    
    try:
        portions = int(update.message.text)
        if portions <= 0:
            raise ValueError("Portions should be greater than zero.")
        
        user_baskets[user_id]['portions'] = portions
        
        # Ask for the delivery time
        await update.message.reply_text(f"How many portions of *{dish_name}* would you like to order? {portions}.\nWhen would you like to have it delivered (in 30 min intervals)?")

    except ValueError:
        await update.message.reply_text("Please enter a valid number of portions.")

# Add more functionality to track delivery time and basket updates as needed


# For storing users' orders
order_list = {}

# Add user to the list
async def add_user_to_list(user_id, user_name, dish_name, portions, delivery_time):
    order_list[user_id] = {
        "user_name": user_name,
        "dish_name": dish_name,
        "portions": portions,
        "delivery_time": delivery_time
    }

# Admin can remove users from the list
async def remove_user_from_list(update: Update, context: CallbackContext):
    user_id = update.message.text.split(" ")[1]  # Admin provides user ID to remove
    if user_id in order_list:
        del order_list[user_id]
        await update.message.reply_text(f"User {user_id} removed from the order list.")
    else:
        await update.message.reply_text("User not found in the list.")


def main():
    app = Application.builder().token(TOKEN).build()

     # Add command handlers
    app.add_handler(CommandHandler("start", welcome_message))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text("Available commands: /start /help")))

    # Callback handlers
    app.add_handler(CallbackQueryHandler(display_menu_of_week, pattern='^menu_of_week$'))  # Handle the callback data
    app.add_handler(CallbackQueryHandler(show_dish_details))  # Catch all dish selections

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()