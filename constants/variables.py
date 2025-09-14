# LibroChef Bot Variables and Constants
# This file contains all the configurable variables, business constants, and data structures

"""
Organization:
- Configuration: Bot settings, tokens, admin info
- Business Logic: Limits, file paths, operational constants  
- Menu Data: Menu items, pricing, availability
- Runtime State: Counters and dynamic data
"""

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

# Bot Authentication
TOKEN = "7803608326:AAGGVhBNpqFS9-ZPkOW35mh8nRFhJaYwnDY"  # Replace with your bot token from BotFather

# Admin Configuration
ADMIN_TELEGRAM_ID = 62355747  # Replace with your actual Telegram ID
CONTACT_ADMIN = "https://t.me/mrlibro"  # Admin contact link

# =============================================================================
# BUSINESS LOGIC CONSTANTS
# =============================================================================

# Order Limits
MAX_PORTIONS = 5  # Maximum total portions that can be ordered per day

# File Paths
ORDERS_LOG_FILE = "orders.txt"  # File to store order history
PORTION_COUNT_FILE = "portion_count.txt"  # File to persist portion count

# Order Constraints
MIN_QUANTITY = 1  # Minimum portions per order
MAX_QUANTITY = 4  # Maximum portions per order (larger orders need admin contact)

# Timing
QUALITY_CHECK_DELAY = 5  # Seconds to wait before sending quality check

# =============================================================================
# MENU DATA CONSTANTS
# =============================================================================

# Weekly Menu Configuration
# This can be easily updated to change the menu offerings
MENU_OF_WEEK = [
    {
        "name": "kir",
        "price": 6,
        "location": "Milan", 
        "time_of_delivery": "13:00-14:00"
    },
    # Add more menu items here as needed
    # {
    #     "name": "another_dish",
    #     "price": 8,
    #     "location": "Rome",
    #     "time_of_delivery": "12:00-13:00"
    # }
]

# Available Delivery Addresses
DELIVERY_ADDRESSES = [
    {"name": "Loreto Square", "code": "Loreto"},
    {"name": "Politecnico di Milano - Piola", "code": "Piola"}
]

# Available Days for Delivery
AVAILABLE_DAYS = ["Saturday", "Sunday"]  # Can be expanded as needed

# =============================================================================
# RUNTIME STATE VARIABLES
# =============================================================================

# Current Portions Counter (will be loaded from file on startup)
current_portions_count = 0  # Tracks sum of all portions ordered today

# =============================================================================
# HELPER FUNCTIONS FOR CONSTANTS
# =============================================================================

def get_current_menu():
    """
    Get the current menu. In the future, this could be enhanced to:
    - Load from database
    - Filter by availability
    - Apply seasonal changes
    """
    return MENU_OF_WEEK

def get_delivery_addresses():
    """Get available delivery addresses"""
    return DELIVERY_ADDRESSES

def get_available_days():
    """Get available delivery days"""
    return AVAILABLE_DAYS

def is_within_portion_limit(additional_quantity):
    """Check if adding quantity would exceed the daily limit"""
    return (current_portions_count + additional_quantity) <= MAX_PORTIONS

def get_remaining_portions():
    """Get how many more portions can be ordered today"""
    return max(0, MAX_PORTIONS - current_portions_count)

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def is_valid_quantity(quantity):
    """Check if the quantity is within acceptable range"""
    try:
        qty = int(quantity)
        return MIN_QUANTITY <= qty <= MAX_QUANTITY
    except (ValueError, TypeError):
        return False

def find_dish_by_name(dish_name):
    """Find a dish in the menu by name"""
    return next((dish for dish in MENU_OF_WEEK if dish['name'] == dish_name), None)

# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

def validate_configuration():
    """
    Validate that all required configuration is present
    Call this on startup to ensure everything is properly configured
    """
    errors = []
    
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        errors.append("Bot TOKEN is not configured")
    
    if not ADMIN_TELEGRAM_ID:
        errors.append("ADMIN_TELEGRAM_ID is not configured")
    
    if not MENU_OF_WEEK:
        errors.append("MENU_OF_WEEK is empty")
    
    if MAX_PORTIONS <= 0:
        errors.append("MAX_PORTIONS must be greater than 0")
    
    return errors

# =============================================================================
# EXPORT LIST
# =============================================================================

# Define what should be available when importing from this module
__all__ = [
    # Configuration
    'TOKEN', 'ADMIN_TELEGRAM_ID', 'CONTACT_ADMIN',
    
    # Business Logic
    'MAX_PORTIONS', 'ORDERS_LOG_FILE', 'PORTION_COUNT_FILE',
    'MIN_QUANTITY', 'MAX_QUANTITY', 'QUALITY_CHECK_DELAY',
    
    # Menu Data
    'MENU_OF_WEEK', 'DELIVERY_ADDRESSES', 'AVAILABLE_DAYS',
    
    # Runtime State
    'current_portions_count',
    
    # Helper Functions
    'get_current_menu', 'get_delivery_addresses', 'get_available_days',
    'is_within_portion_limit', 'get_remaining_portions',
    'is_valid_quantity', 'find_dish_by_name', 'validate_configuration'
]
