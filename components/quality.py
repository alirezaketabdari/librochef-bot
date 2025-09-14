"""Quality component - handles quality feedback system"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from datetime import datetime
import logging
from constants.texts import texts
from constants.variables import ADMIN_TELEGRAM_ID

async def send_quality_check(context: CallbackContext, user_id: int, order_details: dict):
    """Send a quality check message to the user"""
    try:
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

        await context.bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Error sending quality check: {e}")

async def handle_quality_feedback(update: Update, context: CallbackContext):
    """Handle the initial quality rating"""
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    quality = data[1]
    user_id = data[2]

    context.user_data["quality_rating"] = quality
    context.user_data["awaiting_feedback_text"] = True

    rating_type = texts.POSITIVE_RATING if quality == 'good' else texts.CONSTRUCTIVE_RATING
    await query.edit_message_text(
        f"Thank you for your {rating_type} rating!\n\n"
        f"{texts.ADDITIONAL_COMMENTS_PROMPT}",
        parse_mode="Markdown"
    )

async def receive_feedback_text(update: Update, context: CallbackContext):
    """Process the detailed feedback text"""
    if not context.user_data.get("awaiting_feedback_text"):
        return

    if "quality_rating" not in context.user_data:
        return

    feedback_text = update.message.text
    user_id = update.message.from_user.id
    quality = context.user_data["quality_rating"]
    username = update.message.from_user.username or "NoUsername"

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
        await update.message.reply_text(texts.THANK_YOU_FEEDBACK)
    except Exception as e:
        logging.error(f"Error sending feedback: {e}")
        await update.message.reply_text(texts.FEEDBACK_ERROR)

    context.user_data.clear()

async def skip_feedback(update: Update, context: CallbackContext):
    """Handle when user skips providing detailed feedback"""
    if not context.user_data.get("awaiting_feedback_text"):
        return

    user_id = update.message.from_user.id
    quality = context.user_data["quality_rating"]
    username = update.message.from_user.username or "NoUsername"

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
        await update.message.reply_text(texts.THANK_YOU_RATING)
    except Exception as e:
        logging.error(f"Error sending feedback: {e}")
        await update.message.reply_text(texts.FEEDBACK_PROCESS_ERROR)

    context.user_data.clear()
