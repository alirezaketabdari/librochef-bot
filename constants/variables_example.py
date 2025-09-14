#!/usr/bin/env python3
"""
Example usage of the LibroChef variables and constants system.

This file demonstrates how to use the organized constants and variables,
similar to how you would organize configuration in larger projects.
"""

# Import the variables and constants
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants.variables import (
    # Configuration
    TOKEN, ADMIN_TELEGRAM_ID, CONTACT_ADMIN,
    # Business Logic
    MAX_PORTIONS, MIN_QUANTITY, MAX_QUANTITY,
    # Menu Data
    MENU_OF_WEEK, DELIVERY_ADDRESSES, AVAILABLE_DAYS,
    # Helper Functions
    get_current_menu, is_within_portion_limit, get_remaining_portions,
    is_valid_quantity, find_dish_by_name, validate_configuration
)

def example_configuration_access():
    """Example of accessing configuration constants"""
    print("=== Configuration Constants ===")
    print(f"Bot Token: {TOKEN[:20]}... (truncated for security)")
    print(f"Admin ID: {ADMIN_TELEGRAM_ID}")
    print(f"Contact Admin: {CONTACT_ADMIN}")

def example_business_logic():
    """Example of using business logic constants"""
    print("\n=== Business Logic Constants ===")
    print(f"Maximum portions per day: {MAX_PORTIONS}")
    print(f"Quantity range: {MIN_QUANTITY} - {MAX_QUANTITY}")
    
    # Test portion limits
    test_quantity = 3
    can_order = is_within_portion_limit(test_quantity)
    remaining = get_remaining_portions()
    
    print(f"Can order {test_quantity} portions: {can_order}")
    print(f"Remaining portions today: {remaining}")

def example_menu_data():
    """Example of working with menu data"""
    print("\n=== Menu Data ===")
    
    # Get current menu
    menu = get_current_menu()
    print("Current menu:")
    for dish in menu:
        print(f"  - {dish['name']}: €{dish['price']} ({dish['location']}, {dish['time_of_delivery']})")
    
    # Find a specific dish
    dish_name = "kir"
    dish = find_dish_by_name(dish_name)
    if dish:
        print(f"\nFound dish '{dish_name}': €{dish['price']}")
    else:
        print(f"\nDish '{dish_name}' not found")
    
    # Show delivery addresses
    print("\nDelivery addresses:")
    for addr in DELIVERY_ADDRESSES:
        print(f"  - {addr['name']} ({addr['code']})")
    
    # Show available days
    print(f"\nAvailable days: {', '.join(AVAILABLE_DAYS)}")

def example_validation():
    """Example of using validation functions"""
    print("\n=== Validation Examples ===")
    
    # Test quantity validation
    test_quantities = [0, 1, 3, 5, 10, "invalid"]
    for qty in test_quantities:
        valid = is_valid_quantity(qty)
        print(f"Quantity {qty}: {'✅ Valid' if valid else '❌ Invalid'}")
    
    # Configuration validation
    print("\nConfiguration validation:")
    errors = validate_configuration()
    if errors:
        print("❌ Configuration issues:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration is valid!")

def example_dynamic_usage():
    """Example of how this would be used in practice"""
    print("\n=== Practical Usage Example ===")
    
    # Simulate checking if an order can be placed
    customer_order = {
        "dish": "kir",
        "quantity": 2,
        "day": "Saturday",
        "address": "Loreto"
    }
    
    print(f"Processing order: {customer_order}")
    
    # Validate dish exists
    dish = find_dish_by_name(customer_order["dish"])
    if not dish:
        print("❌ Dish not available")
        return
    
    # Validate quantity
    if not is_valid_quantity(customer_order["quantity"]):
        print(f"❌ Invalid quantity. Must be between {MIN_QUANTITY} and {MAX_QUANTITY}")
        return
    
    # Check portion limits
    if not is_within_portion_limit(customer_order["quantity"]):
        remaining = get_remaining_portions()
        print(f"❌ Not enough portions available. Only {remaining} left today.")
        return
    
    # Calculate total price
    total_price = dish["price"] * customer_order["quantity"]
    
    print("✅ Order validation successful!")
    print(f"   Dish: {dish['name']}")
    print(f"   Quantity: {customer_order['quantity']}")
    print(f"   Total Price: €{total_price}")
    print(f"   Delivery: {customer_order['day']} to {customer_order['address']}")

if __name__ == "__main__":
    example_configuration_access()
    example_business_logic()
    example_menu_data()
    example_validation()
    example_dynamic_usage()
