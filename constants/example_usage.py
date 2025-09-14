#!/usr/bin/env python3
"""
Example usage of the LibroChef text constants system.

This file demonstrates how to use the text constants in different ways,
similar to how you would use JSON files in JavaScript.
"""

# Import the text manager
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants.texts import texts, get_text

def example_basic_usage():
    """Basic usage examples"""
    print("=== Basic Usage ===")
    
    # Method 1: Using the texts object directly
    print("Welcome message:", texts.WELCOME_TITLE)
    
    # Method 2: Using attribute access
    print("Greeting:", texts.WELCOME_GREETING)
    
    # Method 3: Using dictionary-style access
    print("Bot intro:", texts['WELCOME_BOT_INTRO'])
    
    # Method 4: Using the convenience function
    print("Let's get started:", get_text('LETS_GET_STARTED'))

def example_formatted_text():
    """Examples with text formatting"""
    print("\n=== Formatted Text Examples ===")
    
    # Using format parameters
    error_msg = texts.get('PORTIONS_LIMIT_ERROR', remaining=3)
    print("Error message:", error_msg)
    
    # Using the convenience function with formatting
    success_msg = get_text('PORTIONS_ADDED_SUCCESS', quantity=2, dish='Kir Sandwich')
    print("Success message:", success_msg)

def example_language_switching():
    """Example of switching languages (when more languages are added)"""
    print("\n=== Language Management ===")
    
    # Check current language
    print(f"Current language: {texts.current_language}")
    
    # List available languages
    print(f"Available languages: {texts.get_available_languages()}")
    
    # Note: To add a new language, create a new file like 'it.py' for Italian
    # with the same constant names but translated values

def example_creating_messages():
    """Example of creating complete messages like in the bot"""
    print("\n=== Creating Complete Messages ===")
    
    # Simulate creating a welcome message like in the bot
    welcome_message = (
        f"{texts.WELCOME_TITLE}\n\n"
        f"{texts.WELCOME_GREETING}\n"
        f"{texts.WELCOME_BOT_INTRO}\n\n"
        f"{texts.WHAT_IS_LIBROCHEF_TITLE}\n"
        f"{texts.WHAT_IS_LIBROCHEF_DESC}\n\n"
        f"{texts.HOW_CAN_I_HELP_TITLE}\n"
        f"{texts.HOW_CAN_I_HELP_DESC}\n\n"
        f"{texts.LETS_GET_STARTED}"
    )
    
    print("Complete welcome message:")
    print(welcome_message)

if __name__ == "__main__":
    example_basic_usage()
    example_formatted_text()
    example_language_switching()
    example_creating_messages()
