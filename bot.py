"""
LibroChef Bot - Main Application
Clean, component-based Telegram bot for food ordering
"""

from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters
)

# Import components
from components.welcome import welcome_message
from components.language import handle_language_selection, handle_web_app_data
from components.menu import display_menu_of_week, show_dish_details
from components.ordering import (
    toggle_day, confirm_day, select_address, 
    add_to_basket, receive_quantity
)
from components.quality import (
    handle_quality_feedback, receive_feedback_text, skip_feedback
)
from components.utils import (
    error_handler, setup_logging, validate_startup, load_portions_count
)

# Import constants
from constants.variables import TOKEN

def setup_handlers(app: Application):
    """Configure all bot handlers"""
    # Commands
    app.add_handler(CommandHandler("start", welcome_message))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text("Available commands: /start /help")))
    app.add_handler(CommandHandler("skip", skip_feedback))
    
    # Language selection
    app.add_handler(CallbackQueryHandler(handle_language_selection, pattern=r'^lang_.*'))
    
    # Web App data (for full-page language selection if implemented)
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    
    # Menu flow
    app.add_handler(CallbackQueryHandler(display_menu_of_week, pattern='^menu_of_week$'))
    app.add_handler(CallbackQueryHandler(show_dish_details, pattern=r'^kir$'))
    
    # Ordering flow
    app.add_handler(CallbackQueryHandler(toggle_day, pattern=r"^toggle_.*"))
    app.add_handler(CallbackQueryHandler(confirm_day, pattern="confirm_day"))
    app.add_handler(CallbackQueryHandler(select_address, pattern=r"^address_.*"))
    app.add_handler(CallbackQueryHandler(add_to_basket, pattern=r'^add_.*'))
    
    # Quality feedback
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
    
    # Error handler
    app.add_error_handler(error_handler)

def main():
    """Main application entry point"""
    setup_logging()
    
    if not validate_startup():
        return
    
    load_portions_count()
    
    try:
        app = Application.builder().token(TOKEN).build()
        setup_handlers(app)
        
        print("🤖 LibroChef Bot starting...")
        print("✅ All components loaded")
        print("🚀 Bot is running!")
        
        app.run_polling()
        
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")

if __name__ == "__main__":
    main()
