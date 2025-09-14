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
        'en': f"✅ Language set to {selected_lang}",
        'it': f"✅ Lingua impostata su {selected_lang}",
        'fa': f"✅ زبان به {selected_lang} تنظیم شد"
    }
    
    await query.answer()
    await query.edit_message_text(
        confirmation_text.get(language, confirmation_text['en']),
        parse_mode="Markdown"
    )
    
    # Show LibroChef services after language selection
    services_text = {
        'en': "**LibroChef offers three different services:**\n\n"
              "🍽️ **Weekend Delivery** – Every weekend, LibroChef suggests a special dish. You place your order, and at the scheduled time and date, you receive your meal directly from LibroChef.\n\n"
              "🎉 **Party & Gathering Delivery** – Choose a suitable day from the available slots, pick your favorite items from the menu, and LibroChef delivers them to you at a very affordable cost—perfect for your parties and get-togethers.\n\n"
              "👨‍🍳 **Personal Chef** – This service is still under development. As soon as it's ready, we'll be delighted to share the details with you.",
        
        'it': "**LibroChef offre tre servizi diversi:**\n\n"
              "🍽️ **Consegna Weekend** – Ogni weekend, LibroChef suggerisce un piatto speciale. Fai il tuo ordine e all'orario e data programmati, ricevi il tuo pasto direttamente da LibroChef.\n\n"
              "🎉 **Consegna per Feste e Riunioni** – Scegli un giorno adatto dagli slot disponibili, seleziona i tuoi piatti preferiti dal menu, e LibroChef te li consegna a un costo molto conveniente—perfetto per le tue feste e riunioni.\n\n"
              "👨‍🍳 **Chef Personale** – Questo servizio è ancora in fase di sviluppo. Non appena sarà pronto, saremo felici di condividere i dettagli con te.",
        
        'fa': "**LibroChef سه سرویس مختلف ارائه می‌دهد:**\n\n"
              "🍽️ **تحویل  آخر هفته** – هر آخر هفته، LibroChef یک غذای ویژه پیشنهاد می‌دهد. شما سفارش خود را ثبت می‌کنید و در زمان و تاریخ تعیین شده، غذای خود را مستقیماً از LibroChef دریافت می‌کنید.\n\n"
              "🎉 **تحویل مهمانی و گردهمایی** – روز مناسبی از زمان‌های موجود انتخاب کنید، غذاهای مورد علاقه‌تان را از منو انتخاب کنید، و LibroChef آن‌ها را با قیمت بسیار مقرون به صرفه برای شما تحویل می‌دهد—عالی برای مهمانی‌ها و گردهمایی‌هایتان.\n\n"
              "👨‍🍳 **سرآشپز شخصی** – این سرویس هنوز در حال توسعه است. به محض آماده شدن، خوشحال خواهیم بود جزئیات را با شما به اشتراک بگذاریم."
    }
    
    keyboard = [
        [InlineKeyboardButton("🍽️ Weekend Free Delivery", callback_data='service_weekend')],
        [InlineKeyboardButton("🎉 Party & Gathering Delivery", callback_data='service_party')],
        [InlineKeyboardButton("👨‍🍳 Personal Chef", callback_data='service_chef')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        services_text.get(language, services_text['en']),
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
        # Continue with existing weekend delivery flow
        menu_text = {
            'en': "Please select a dish from the menu of the day:",
            'it': "Seleziona un piatto dal menu del giorno:",
            'fa': "لطفاً یک غذا از منوی روز انتخاب کنید:"
        }
        
        await query.edit_message_text(menu_text.get(language, menu_text['en']))
        
        # Import and continue with existing menu flow
        from components.menu import display_menu_of_week
        await display_menu_of_week(update, context)
        
    elif service in ['party', 'chef']:
        # Show under development message
        under_development_text = {
            'en': "🚧 **This option is under process**\n\nWe're working hard to bring you this amazing service soon! Please check back later or try our Weekend Free Delivery service.",
            'it': "🚧 **Questa opzione è in fase di sviluppo**\n\nStiamo lavorando duramente per portarti presto questo servizio fantastico! Riprova più tardi o prova il nostro servizio di Consegna Gratuita Weekend.",
            'fa': "🚧 **این گزینه در حال پردازش است**\n\nما سخت در حال کار بر روی این سرویس فوق‌العاده هستیم تا به زودی آن را برای شما آماده کنیم! لطفاً بعداً بررسی کنید یا سرویس تحویل رایگان آخر هفته ما را امتحان کنید."
        }
        
        # Back to services button
        keyboard = [[InlineKeyboardButton("🔙 Back to Services", callback_data='back_to_services')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            under_development_text.get(language, under_development_text['en']),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def handle_back_to_services(update: Update, context: CallbackContext):
    """Handle back to services button"""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data.get('language', 'en')
    
    # Show services again
    services_text = {
        'en': "**LibroChef offers three different services:**\n\n"
              "🍽️ **Weekend Free Delivery** – Every weekend, LibroChef suggests a special dish. You place your order, and at the scheduled time and date, you receive your meal directly from LibroChef.\n\n"
              "🎉 **Party & Gathering Delivery** – Choose a suitable day from the available slots, pick your favorite items from the menu, and LibroChef delivers them to you at a very affordable cost—perfect for your parties and get-togethers.\n\n"
              "👨‍🍳 **Personal Chef** – This service is still under development. As soon as it's ready, we'll be delighted to share the details with you.",
        
        'it': "**LibroChef offre tre servizi diversi:**\n\n"
              "🍽️ **Consegna Gratuita Weekend** – Ogni weekend, LibroChef suggerisce un piatto speciale. Fai il tuo ordine e all'orario e data programmati, ricevi il tuo pasto direttamente da LibroChef.\n\n"
              "🎉 **Consegna per Feste e Riunioni** – Scegli un giorno adatto dagli slot disponibili, seleziona i tuoi piatti preferiti dal menu, e LibroChef te li consegna a un costo molto conveniente—perfetto per le tue feste e riunioni.\n\n"
              "👨‍🍳 **Chef Personale** – Questo servizio è ancora in fase di sviluppo. Non appena sarà pronto, saremo felici di condividere i dettagli con te.",
        
        'fa': "**LibroChef سه سرویس مختلف ارائه می‌دهد:**\n\n"
              "🍽️ **تحویل رایگان آخر هفته** – هر آخر هفته، LibroChef یک غذای ویژه پیشنهاد می‌دهد. شما سفارش خود را ثبت می‌کنید و در زمان و تاریخ تعیین شده، غذای خود را مستقیماً از LibroChef دریافت می‌کنید.\n\n"
              "🎉 **تحویل مهمانی و گردهمایی** – روز مناسبی از زمان‌های موجود انتخاب کنید، غذاهای مورد علاقه‌تان را از منو انتخاب کنید، و LibroChef آن‌ها را با قیمت بسیار مقرون به صرفه برای شما تحویل می‌دهد—عالی برای مهمانی‌ها و گردهمایی‌هایتان.\n\n"
              "👨‍🍳 **سرآشپز شخصی** – این سرویس هنوز در حال توسعه است. به محض آماده شدن، خوشحال خواهیم بود جزئیات را با شما به اشتراک بگذاریم."
    }
    
    keyboard = [
        [InlineKeyboardButton("🍽️ Weekend Free Delivery", callback_data='service_weekend')],
        [InlineKeyboardButton("🎉 Party & Gathering Delivery", callback_data='service_party')],
        [InlineKeyboardButton("👨‍🍳 Personal Chef", callback_data='service_chef')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        services_text.get(language, services_text['en']),
        parse_mode="Markdown",
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
