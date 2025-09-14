"""Language selection component - handles language selection with beautiful web interface"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import CallbackContext
import json
from constants.texts import texts

async def show_language_selection(update: Update, context: CallbackContext):
    """Show beautiful language selection page"""
    
    # Option 1: Web App (uncomment if you want to use the full-page HTML interface)
    # from telegram import WebAppInfo
    # web_app = WebAppInfo(url="http://localhost:5000/welcome")  # or your hosted URL
    # keyboard = [[InlineKeyboardButton("🌍 Choose Language", web_app=web_app)]]
    
    # Option 2: Rich inline keyboard with beautiful styling (current implementation)
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
        [InlineKeyboardButton("🇮🇹 Italiano", callback_data='lang_it')],
        [InlineKeyboardButton("🇮🇷 فارسی", callback_data='lang_fa')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🍽️ **LibroChef Bot** 🍽️\n\n"
        "🇬🇧 **Welcome to LibroChef bot,**\n"
        "**Which language do you prefer?**\n\n"
        "🇮🇹 **Benvenuto nel bot LibroChef,**\n"
        "**Quale lingua preferisci?**\n\n"
        "🇮🇷 **به ربات LibroChef خوش آمدید،**\n"
        "**کدام زبان را ترجیح می‌دهید؟**"
    )
    
    await update.effective_message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def handle_language_selection(update: Update, context: CallbackContext):
    """Handle language selection from buttons"""
    query = update.callback_query
    language = query.data.split('_')[1]  # Extract language code
    
    # Store selected language
    context.user_data['language'] = language
    
    # Set the language in texts system
    texts.set_language(language)
    
    # Show confirmation and proceed to main menu
    language_names = {
        'en': '🇬🇧 English',
        'it': '🇮🇹 Italiano', 
        'fa': '🇮🇷 فارسی'
    }
    
    selected_lang = language_names.get(language, 'English')
    
    await query.answer()
    await query.edit_message_text(
        texts.get("LANGUAGE_SET_CONFIRMATION", language=selected_lang),
        parse_mode="Markdown"
    )
    
    # Show LibroChef services after language selection
    keyboard = [
        [InlineKeyboardButton(texts.WEEKEND_DELIVERY_BUTTON, callback_data='service_weekend')],
        [InlineKeyboardButton(texts.PARTY_DELIVERY_BUTTON, callback_data='service_party')],
        [InlineKeyboardButton(texts.PERSONAL_CHEF_BUTTON, callback_data='service_chef')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        texts.SERVICES_INTRO,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def handle_service_selection(update: Update, context: CallbackContext):
    """Handle service selection from buttons"""
    query = update.callback_query
    await query.answer()
    
    service = query.data.split('_')[1]  # Extract service type
    language = context.user_data.get('language', 'en')
    
    if service == 'weekend':
        # Continue with existing weekend delivery flow (no menu prompt needed since there's only one dish)
        from components.menu import display_menu_of_week
        await display_menu_of_week(update, context)
        
    elif service in ['party', 'chef']:
        # Show under development message
        keyboard = [[InlineKeyboardButton(texts.BACK_TO_SERVICES_BUTTON, callback_data='back_to_services')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            texts.SERVICE_UNDER_DEVELOPMENT,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def handle_back_to_services(update: Update, context: CallbackContext):
    """Handle back to services button"""
    query = update.callback_query
    await query.answer()
    
    # Show services again using centralized text system
    keyboard = [
        [InlineKeyboardButton(texts.WEEKEND_DELIVERY_BUTTON, callback_data='service_weekend')],
        [InlineKeyboardButton(texts.PARTY_DELIVERY_BUTTON, callback_data='service_party')],
        [InlineKeyboardButton(texts.PERSONAL_CHEF_BUTTON, callback_data='service_chef')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        texts.SERVICES_INTRO,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def handle_back_to_start(update: Update, context: CallbackContext):
    """Handle back to start button - restart the language selection"""
    query = update.callback_query
    
    # Clear user data and restart
    context.user_data.clear()
    
    await query.answer()
    await show_language_selection(update, context)

async def handle_web_app_data(update: Update, context: CallbackContext):
    """Handle data from web app (if using web app version)"""
    try:
        data = json.loads(update.effective_message.web_app_data.data)
        if data.get('action') == 'select_language':
            language = data.get('language')
            context.user_data['language'] = language
            texts.set_language(language)
            
            # Continue with bot flow
            await update.effective_message.reply_text(
                f"✅ Language set! Welcome to LibroChef! 🍽️"
            )
            
    except Exception as e:
        await update.effective_message.reply_text("Error processing language selection.")
