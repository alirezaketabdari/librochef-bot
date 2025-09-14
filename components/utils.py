"""Utils component - utility functions and error handling"""

from telegram import Update
from telegram.ext import CallbackContext
import logging
from constants.texts import texts
from constants.variables import (
    CONTACT_ADMIN, PORTION_COUNT_FILE, validate_configuration
)
import constants.variables as vars_module

def load_portions_count():
    """Load portion count from file and update the global variable"""
    try:
        with open(PORTION_COUNT_FILE, 'r', encoding='utf-8') as f:
            vars_module.current_portions_count = int(f.read().strip())
            print(f"📊 Loaded portion count: {vars_module.current_portions_count}/{vars_module.MAX_PORTIONS}")
    except (FileNotFoundError, ValueError) as e:
        vars_module.current_portions_count = 0
        print(f"📊 Portion count file issue ({e}), starting with 0")

def is_expecting_quantity(context: CallbackContext) -> bool:
    """Check if user is in quantity input mode"""
    return context.user_data.get("awaiting_quantity", False)

def is_expecting_feedback(context: CallbackContext) -> bool:
    """Check if user is in feedback input mode"""
    return context.user_data.get("awaiting_feedback_text", False)

async def error_handler(update: Update, context: CallbackContext):
    """Handle errors and notify user"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.error("Exception while handling an update:", exc_info=context.error)
    
    # Only try to send error message if we have a valid update with message capability
    try:
        if update and hasattr(update, 'effective_message') and update.effective_message:
            await update.effective_message.reply_text(
                "C'è un problema con il bot. Riprova più tardi o contatta l'admin: Contact Admin (https://t.me/mrlibro)"
            )
        elif update and hasattr(update, 'message') and update.message:
            await update.message.reply_text(
                "C'è un problema con il bot. Riprova più tardi o contatta l'admin: Contact Admin (https://t.me/mrlibro)"
            )
    except Exception as e:
        logger.error(f"Error sending error message: {e}")
        # Don't try to send another message, just log it

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def validate_startup():
    """Validate configuration on startup"""
    config_errors = validate_configuration()
    if config_errors:
        print("❌ Configuration errors found:")
        for error in config_errors:
            print(f"  - {error}")
        print("Please fix these issues before starting the bot.")
        return False
    
    print("✅ Configuration validated successfully!")
    return True
