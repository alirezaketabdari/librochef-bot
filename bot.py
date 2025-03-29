from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from urllib.parse import quote, unquote
# Replace this with your bot token from BotFather 
TOKEN = "7803608326:AAGGVhBNpqFS9-ZPkOW35mh8nRFhJaYwnDY"


# Send automatic introduction when the user first interacts with the bot
async def welcome_message(update: Update, context: CallbackContext):
    intro_text = (
        "🍽️ *Welcome to LibroChef Bot!* 🍽️\n\n"
        "Hey there! 👋 \n" 
        "I'm *LibroChef Bot*, your foodie companion, here to make your culinary experience smooth and delicious. 🍲🔥\n\n"
        
        "🌟 *What is LibroChef?* 🌟\n"
        "LibroChef is a *culinary studio* where we cook, learn, and experiment—from *classic dishes* to *modern gastronomy*. "
        "We love pushing boundaries with *new techniques, large-scale catering, and creative recipes*.\n\n"

        "🤖 *How Can I Help?* 🤖\n"
        "I handle *deliveries* and sign you up for *exclusive culinary events*. Need our *weekly menu*? I've got you covered! 🍕📦\n\n"
        
        "🚀 Let’s get started!!"
    )

    # Create a button that triggers the /menuOfWeek command
    keyboard = [
        [InlineKeyboardButton("Show Menu of the Week", callback_data='menu_of_week')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the welcome message with the button
    await update.message.reply_text(intro_text, parse_mode="Markdown", reply_markup=reply_markup)

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
    print(dish)
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
        callback_data = f"add_{quote(dish_name)}"
        print(callback_data)
        keyboard = [[InlineKeyboardButton("🛒 Add to Basket", callback_data=callback_data)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text("Would you like to add this dish to your basket?", reply_markup=reply_markup)
    else:
        await query.answer("Dish not found.")

# To track the basket (user orders)
user_baskets = {}

# Add dish to the basket
async def add_to_basket(update: Update, context: CallbackContext):
    query = update.callback_query
    dish_name = query.data.split("_", 1)[1]

    # Ask the user for the number of portions
    await query.answer()
    await query.message.reply_text(
        f"How many portions of *{dish_name}* would you like to order?\n\n"
        "🔢 *Enter a number (1-4).*\n"
        "⚠️ If you need more than 4 portions, please contact the admin: [Contact Admin](https://t.me/mrlibro)",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    # Save dish name in context
    context.user_data["pending_order"] = {"dish": dish_name}

    # Set up a message handler to capture user input
    context.user_data["awaiting_quantity"] = True

async def receive_quantity(update: Update, context: CallbackContext):
    if "awaiting_quantity" not in context.user_data:
        return  # Ignore messages if not expecting input

    user_input = update.message.text.strip()

    if not user_input.isdigit():
        await update.message.reply_text("❌ Please enter a valid *number* (1-4). Try again:")
        return

    quantity = int(user_input)

    if quantity > 4:
        await update.message.reply_text(
            "⚠️ Orders of more than 4 portions require admin approval.\n"
            "Please contact the admin: [Contact Admin](https://t.me/mrlibro)",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

    # Save the order
    user_id = update.message.from_user.id
    dish_name = context.user_data["pending_order"]["dish"]
    user_baskets[user_id] = {"dish": dish_name, "portions": quantity}

    await update.message.reply_text(f"✅ *{quantity}* portions of *{dish_name}* added to your basket!", parse_mode="Markdown")

    # Clean up context
    del context.user_data["pending_order"]
    del context.user_data["awaiting_quantity"]


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
    app.add_handler(CallbackQueryHandler(show_dish_details, pattern=r'^(?!add_).*'))  # Catch all dish selections
    app.add_handler(CallbackQueryHandler(add_to_basket, pattern=r'^add_.*'))  # Handle "Add to Basket"

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_quantity))  # Handle user input


    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()