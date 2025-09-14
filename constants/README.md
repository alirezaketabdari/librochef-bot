# LibroChef Constants

This folder contains all the constants used in the LibroChef bot, organized in a clean and maintainable way.

## Structure

```
constants/
├── __init__.py              # Package initialization
├── variables.py             # All constants and variables
├── variables_example.py     # Variables usage examples
├── texts/                   # Text constants for different languages
│   ├── __init__.py          # Easy imports
│   ├── texts.py             # Text management system
│   └── en.py               # English text constants
├── example_usage.py         # Text usage examples
└── README.md               # This file
```

## Usage

### Text Constants

```python
from constants.texts import texts

# Access text constants
welcome = texts.WELCOME_TITLE
greeting = texts.WELCOME_GREETING

# Or use dictionary-style access
welcome = texts['WELCOME_TITLE']
```

### Variables and Configuration

```python
from constants.variables import (
    TOKEN, ADMIN_TELEGRAM_ID, CONTACT_ADMIN,     # Configuration
    MAX_PORTIONS, MIN_QUANTITY, MAX_QUANTITY,    # Business logic
    MENU_OF_WEEK, DELIVERY_ADDRESSES,           # Menu data
    get_current_menu, is_valid_quantity          # Helper functions
)

# Use configuration constants
bot_token = TOKEN
max_daily_portions = MAX_PORTIONS

# Use helper functions
menu = get_current_menu()
if is_valid_quantity(3):
    print("Valid quantity!")
```

### All-in-One Import

```python
from constants import *

# Now you have access to everything:
# - All text constants via 'texts'
# - All variables and configuration constants
# - All helper functions
```

### Formatted Text

```python
from constants.texts import texts, get_text

# Using the get method with formatting
error_msg = texts.get('PORTIONS_LIMIT_ERROR', remaining=3)

# Using the convenience function
success_msg = get_text('PORTIONS_ADDED_SUCCESS', quantity=2, dish='Sandwich')
```

### In Your Bot Code

```python
from constants.texts import texts

# Instead of hardcoded strings:
# await update.message.reply_text("🍽️ Welcome to LibroChef Bot! 🍽️")

# Use constants:
await update.message.reply_text(texts.WELCOME_TITLE)
```

## Adding New Languages

To add support for a new language (e.g., Italian):

1. Create a new file `it.py` in the `texts/` folder
2. Copy all the constants from `en.py`
3. Translate the values to Italian
4. Switch language in your code:

```python
from constants.texts import texts

# Switch to Italian
texts.set_language('it')
```

## Types of Constants

### Configuration Constants
These are sensitive settings that should be configured before deployment:
- `TOKEN`: Bot token from BotFather
- `ADMIN_TELEGRAM_ID`: Your Telegram user ID
- `CONTACT_ADMIN`: Admin contact link

### Business Logic Constants
These control how your bot operates:
- `MAX_PORTIONS`: Daily portion limit
- `MIN_QUANTITY`/`MAX_QUANTITY`: Order size limits
- `QUALITY_CHECK_DELAY`: Timing for quality checks

### Menu Data Constants
These define your menu and delivery options:
- `MENU_OF_WEEK`: Available dishes
- `DELIVERY_ADDRESSES`: Where you deliver
- `AVAILABLE_DAYS`: When you deliver

### Helper Functions
Smart functions that work with your constants:
- `get_current_menu()`: Get available dishes
- `is_valid_quantity()`: Validate order quantities
- `find_dish_by_name()`: Search menu items
- `validate_configuration()`: Check setup

## Benefits

- **Centralized**: All constants in organized files
- **Maintainable**: Easy to update settings and messages
- **Multilingual**: Easy to add new languages
- **Type-safe**: Constants are clearly defined
- **Flexible**: Supports string formatting and validation
- **Scalable**: Organized for growth
- **Similar to JavaScript**: Works like JSON files but more powerful

## Example

Instead of scattered hardcoded strings throughout your code:

```python
# ❌ Hard to maintain
await update.message.reply_text("🍽️ Welcome to LibroChef Bot! 🍽️")
await update.message.reply_text("❌ We're completely full for today!")
```

You now have organized, reusable constants:

```python
# ✅ Easy to maintain and translate
await update.message.reply_text(texts.WELCOME_TITLE)
await update.message.reply_text(texts.COMPLETELY_FULL_MESSAGE)
```
