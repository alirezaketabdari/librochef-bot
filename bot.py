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
from components.language import (
    handle_language_selection, handle_web_app_data, 
    handle_service_selection, handle_back_to_services
)
from components.menu import display_menu_of_week, show_dish_details
from components.ordering import (
    show_portion_selection, handle_portion_selection
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
    
    # Service selection
    app.add_handler(CallbackQueryHandler(handle_service_selection, pattern=r'^service_.*'))
    app.add_handler(CallbackQueryHandler(handle_back_to_services, pattern=r'^back_to_services$'))
    
    # Web App data (for full-page language selection if implemented)
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    
    # Menu flow
    app.add_handler(CallbackQueryHandler(display_menu_of_week, pattern='^menu_of_week$'))
    app.add_handler(CallbackQueryHandler(show_dish_details, pattern=r'^gormeh_sabzi$'))
    
    # Ordering flow (streamlined)
    app.add_handler(CallbackQueryHandler(show_portion_selection, pattern=r'^proceed_to_address$'))
    app.add_handler(CallbackQueryHandler(handle_portion_selection, pattern=r'^portion_\d+$'))
    
    # Quality feedback
    app.add_handler(CallbackQueryHandler(handle_quality_feedback, pattern=r'^quality_(good|bad)_\d+$'))
    
    # Message handlers (only feedback now)
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
        print("💡 Press Ctrl+C to stop the bot")
        
        # Run with drop_pending_updates to clear conflicts
        app.run_polling(drop_pending_updates=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot startup error: {e}")
        print("💡 Try running: python fix_bot_conflicts.py")

if __name__ == "__main__":
    main()
