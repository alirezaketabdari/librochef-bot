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
    
    confirmation_text = {
        'en': f"✅ Language set to {selected_lang}\n\nWelcome to LibroChef! 🍽️",
        'it': f"✅ Lingua impostata su {selected_lang}\n\nBenvenuto in LibroChef! 🍽️",
        'fa': f"✅ زبان به {selected_lang} تنظیم شد\n\n!به LibroChef خوش آمدید 🍽️"
    }
    
    await query.answer()
    await query.edit_message_text(
        confirmation_text.get(language, confirmation_text['en']),
        parse_mode="Markdown"
    )
    
    # Import and show main menu after language selection
    from components.menu import display_menu_of_week
    
    # Create a new update object to show menu
    keyboard = [[InlineKeyboardButton("📋 Show Menu", callback_data='menu_of_week')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    menu_prompt = {
        'en': "Ready to order? 🍴",
        'it': "Pronto per ordinare? 🍴", 
        'fa': "آماده سفارش؟ 🍴"
    }
    
    await query.message.reply_text(
        menu_prompt.get(language, menu_prompt['en']),
        reply_markup=reply_markup
    )

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
