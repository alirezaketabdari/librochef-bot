"""Utils component - utility functions and error handling"""

from telegram import Update
from telegram.ext import CallbackContext
import logging
from constants.texts import texts
from constants.variables import (
    CONTACT_ADMIN, PORTION_COUNT_FILE, validate_configuration, current_portions_count
)

def load_portions_count():
    """Load portion count from file"""
    global current_portions_count
    try:
        with open(PORTION_COUNT_FILE, 'r') as f:
            current_portions_count = int(f.read())
    except (FileNotFoundError, ValueError):
        current_portions_count = 0

def is_expecting_quantity(context: CallbackContext) -> bool:
    """Check if user is in quantity input mode"""
    return context.user_data.get("awaiting_quantity", False)

def is_expecting_feedback(context: CallbackContext) -> bool:
    """Check if user is in feedback input mode"""
    return context.user_data.get("awaiting_feedback_text", False)

async def error_handler(update: Update, context: CallbackContext):
    """Handle errors and notify user"""
    try:
        await update.message.reply_text(
            texts.get("BOT_ERROR_MESSAGE", contact_admin=CONTACT_ADMIN),
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Error sending message: {e}")

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
