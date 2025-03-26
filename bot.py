from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace this with your bot token from BotFather gggggggggggggggg
TOKEN = "7803608326:AAGGVhBNpqFS9-ZPkOW35mh8nRFhJaYwnDY"

# Command Handlers
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I am your Telegram bot 🤖")

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Available commands: /start /help")

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()