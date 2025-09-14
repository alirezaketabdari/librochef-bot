"""Welcome component - handles welcome message and help"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from constants.texts import texts

async def welcome_message(update: Update, context: CallbackContext):
    """Send welcome message with menu button"""
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

    keyboard = [
        [InlineKeyboardButton(texts.SHOW_MENU_BUTTON, callback_data='menu_of_week')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text(intro_text, parse_mode="Markdown", reply_markup=reply_markup)
