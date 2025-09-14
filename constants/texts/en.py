# English text constants
# This file contains all the hardcoded text strings used in the bot

# Welcome and intro messages
WELCOME_TITLE = "🍽️ *Welcome to LibroChef Bot!* 🍽️"
WELCOME_GREETING = "Hey there! 👋"
WELCOME_BOT_INTRO = "I'm *LibroChef Bot*, your foodie companion, here to make your culinary experience smooth and delicious. 🍲🔥"

WHAT_IS_LIBROCHEF_TITLE = "🌟 *What is LibroChef?* 🌟"
WHAT_IS_LIBROCHEF_DESC = ("LibroChef is a *culinary studio* where we cook, learn, and experiment—from *classic dishes* "
                         "to *modern gastronomy*. We love pushing boundaries with *new techniques, large-scale catering, "
                         "and creative recipes*.")

HOW_CAN_I_HELP_TITLE = "🤖 *How Can I Help?* 🤖"
HOW_CAN_I_HELP_DESC = ("I handle *deliveries* and sign you up for *exclusive culinary events*. "
                      "Need our *weekly menu*? I've got you covered! 🍕📦")

LETS_GET_STARTED = "🚀 Let's get started!!"

# Button texts
SHOW_MENU_BUTTON = "Show Menu of the day"

# Menu details
MENU_PACK_PREFIX = "🍽 *pack of 2"
CUTLET_COUNT_TEXT = "*Number of cutlet in each Sandwichwwwwwwwwwwwwwwwwwwwwwwwwwwwwww:* 3"
PRICE_TEXT = "💰 *Price:* €"
MEAT_TEXT = "*Meat (beef):* 100gr"
EGG_TEXT = "*egg:* 1"
POTATO_TEXT = "*potato:* 1"
ONION_TEXT = "*onion:* 1"
GARLIC_TEXT = "*clove of garlic:* 1"
SANDWICH_INSIDE_TEXT = "*Inside the sandwich:* fresh tomato slices, pickles, fresh parsley, sliced onion"
SERVED_WITH_TEXT = "🍽 *sandwich is served with homemade lavash bread and homemade pickles*"
ALLERGEN_INFO_TEXT = "❗ *Allergen information:* contains egg, gluten, garlic,and onion."
DELIVERY_TIME_TEXT = "⏰ *Delivery Time:*"
LOCATION_TEXT = "📍 *Location:*"
MEAT_QUALITY_TEXT = "The meat is provided freshly from the well-known supermarkets."
SELECT_DELIVERY_DAY_TEXT = "📅 *Please select your delivery day:*"

# Error messages
COMPLETELY_FULL_MESSAGE = "❌ We're completely full for today! Please try again tomorrow."
QUANTITY_LIMIT_EXCEEDED = "❌ Sorry, adding {quantity} portions would exceed our daily limit of {max_portions}. We currently have {current} portions ordered."
INVALID_QUANTITY_MESSAGE = "❌ Please enter a valid quantity (1-10)."
NO_MENU_AVAILABLE = "❌ No menu available for today."

# Order messages
ORDER_CONFIRMATION_TITLE = "✅ *Order Confirmation*"
ORDER_DETAILS_PREFIX = "📋 *Order Details:*"
DISH_NAME_TEXT = "🍽 *Dish:*"
QUANTITY_TEXT = "📦 *Quantity:*"
TOTAL_PRICE_TEXT = "💰 *Total Price:* €"
CUSTOMER_INFO_TEXT = "👤 *Customer Info:*"
DELIVERY_DATE_TEXT = "📅 *Delivery Date:*"
ORDER_ID_TEXT = "🆔 *Order ID:*"
ORDER_TIME_TEXT = "⏰ *Order Time:*"

# Admin messages
ADMIN_NOTIFICATION_TITLE = "🔔 *New Order Received!*"
ADMIN_CONTACT_TEXT = "📞 *Contact Admin:*"

# Buttons
ORDER_BUTTON = "🛒 Order"
CONFIRM_ORDER_BUTTON = "✅ Confirm Order"
CANCEL_ORDER_BUTTON = "❌ Cancel"
BACK_TO_MENU_BUTTON = "⬅️ Back to Menu"

# Days of the week
MONDAY = "Monday"
TUESDAY = "Tuesday"
WEDNESDAY = "Wednesday"
THURSDAY = "Thursday"
FRIDAY = "Friday"
SATURDAY = "Saturday"
SUNDAY = "Sunday"

# Quantity options
QUANTITY_OPTIONS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

# Success messages
ORDER_PLACED_SUCCESS = "🎉 Your order has been placed successfully!"
ADMIN_NOTIFIED = "📱 The admin has been notified about your order."

# Input prompts
ENTER_QUANTITY_PROMPT = "Please enter the quantity (1-10):"
ENTER_FULL_NAME_PROMPT = "Please enter your full name:"
ENTER_PHONE_PROMPT = "Please enter your phone number:"
ENTER_ADDRESS_PROMPT = "Please enter your delivery address:"

# Validation messages
INVALID_INPUT = "❌ Invalid input. Please try again."
REQUIRED_FIELD = "❌ This field is required."

# Additional messages found in bot
NEW_ORDER_RECEIVED = "📝 *New Order Received!*"
USER_TEXT = "👤 *User:*"
PORTIONS_TEXT = "🔢 *Portions:*"
QUALITY_CHECK_TITLE = "📝 *Quality Check*"
QUALITY_RATING_PROMPT = "How would you rate the quality of your order?\n\nAfter selecting your rating, you'll be able to add additional comments."
QUALITY_FEEDBACK_RECEIVED = "📊 *Quality Feedback Received*"
RATING_TEXT = "⭐ Rating:"
FEEDBACK_TEXT = "📝 Feedback:"
TIME_TEXT = "🕒 Time:"
THANK_YOU_FEEDBACK = "✅ Thank you for your feedback! We appreciate your time."
THANK_YOU_RATING = "✅ Thank you for your rating!"
FEEDBACK_ERROR = "⚠️ Couldn't send your feedback. Please try again later."
FEEDBACK_PROCESS_ERROR = "⚠️ Couldn't process your request. Please try again later."
POSITIVE_RATING = "👍 positive"
CONSTRUCTIVE_RATING = "👎 constructive"
ADDITIONAL_COMMENTS_PROMPT = "✍️ Please share any additional comments about your experience (or type /skip if you don't want to add comments):"
NO_ADDITIONAL_COMMENTS = "No additional comments"
PORTIONS_ADDED_SUCCESS = "✅ *{quantity}* portions of *{dish}* added to your basket!"
PRE_RESERVATION_MESSAGE = "🎉 This is a pre-reservation. We will contact you to confirm the reservation."
PLACE_ANOTHER_ORDER = "🔄 To place another order, please use /start"
BOT_ERROR_MESSAGE = "There is an issue with the bot. Please try again later or contact the admin: [Contact Admin]({contact_admin})"
DISH_NOT_FOUND = "Dish not found."
# Weekly dish display format
WEEKLY_DISH_TITLE = "🍽️✨ **THIS WEEK LIBROCHEF OFFERS {dish_name}** ✨🍽️"
DELIVERY_DAY_TITLE = "📅🌟 **!! {day} !!** 🌟📅"
PRICE_TITLE = "💰 **Price:** €{price}"
INGREDIENTS_TITLE = "🥘 **Ingredients:**"
ALLERGENS_TITLE = "⚠️ **Allergens:**"
NUTRITION_TITLE = "📊 **Nutritional Values (per serving):**"
EXTRA_INFO_TITLE = "ℹ️ **Extra Information:**"
ORDER_BUTTON_TEXT = "🛒 **ORDER NOW**"
PORTION_SELECTION_TITLE = "🔢 **How many portions would you like to order?**\n\nChoose your portion size below:"
PORTION_1_BUTTON = "1️⃣ 1 portion"
PORTION_2_BUTTON = "2️⃣ 2 portions" 
PORTION_3_BUTTON = "3️⃣ 3 portions"
PORTION_4_BUTTON = "4️⃣ 4 portions"
CONTACT_ADMIN_MORE_BUTTON = "📞 Contact Admin for more"
FULLY_RESERVED_MESSAGE = "🚫 **This delivery is fully reserved**\n\nPlease wait for the next week's menu. We'll be back with delicious new dishes!"

SELECT_DISH_PROMPT = "Please select a dish from the menu of the day:"
SELECT_AT_LEAST_ONE_DAY = "❌ Please select at least one day!"
DELIVERY_SELECTED = "✅ You selected *{days}* for delivery.\n\n📌 *Please select your delivery address:*"
ADDRESS_SELECTED = "📍 You selected *{address}* as the delivery address.\n\n📅 Delivery day(s): *{days}*\n\nTap below to add to your basket:"
ADD_TO_BASKET_BUTTON = "🛒 Add to Basket"
QUANTITY_RANGE_ERROR = "⚠️ Please enter a number between 1 and 4.\nFor larger orders, contact the admin: [Contact Admin](https://t.me/mrlibro)"
PORTIONS_LIMIT_ERROR = "❌ We can only accept {remaining} more portions today. Please order a smaller quantity or try again tomorrow."

# Service selection texts
SERVICES_INTRO = "**LibroChef offers three different services:**\n\n🍽️ **Weekend Delivery** – Every weekend, LibroChef suggests a special dish. You place your order, and at the scheduled time and date, you receive your meal directly from LibroChef.\n\n🎉 **Party & Gathering Delivery** – Choose a suitable day from the available slots, pick your favorite items from the menu, and LibroChef delivers them to you at a very affordable cost—perfect for your parties and get-togethers.\n\n👨‍🍳 **Personal Chef** – This service is still under development. As soon as it's ready, we'll be delighted to share the details with you."

# Service buttons
WEEKEND_DELIVERY_BUTTON = "🍽️ Weekend Free Delivery"
PARTY_DELIVERY_BUTTON = "🎉 Party & Gathering Delivery"
PERSONAL_CHEF_BUTTON = "👨‍🍳 Personal Chef"

# Service flow texts (removed duplicate menu prompt since there's only one dish)
SERVICE_UNDER_DEVELOPMENT = "🚧 **This option is under process**\n\nWe're working hard to bring you this amazing service soon! Please check back later or try our Weekend Free Delivery service."
BACK_TO_SERVICES_BUTTON = "🔙 Back to Services"

# Language selection
LANGUAGE_SET_CONFIRMATION = "✅ Language set to {language}"
