# Text management system for LibroChef Bot
# This module handles text constants and supports multiple languages

import os
from typing import Dict, Any

class TextManager:
    """
    Manages text constants for different languages.
    Similar to how you would handle JSON files in JavaScript, but more Pythonic.
    """
    
    def __init__(self, default_language: str = 'en'):
        self.default_language = default_language
        self.current_language = default_language
        self._texts: Dict[str, Any] = {}
        self._load_language(default_language)
    
    def _load_language(self, language: str) -> None:
        """Load text constants for a specific language"""
        try:
            # Dynamically import the language module
            language_module = __import__(f'constants.texts.{language}', fromlist=[''])
            
            # Get all constants from the module (uppercase variables)
            self._texts = {
                key: getattr(language_module, key) 
                for key in dir(language_module) 
                if key.isupper() and not key.startswith('_')
            }
        except ImportError:
            if language != self.default_language:
                print(f"Warning: Language '{language}' not found, falling back to '{self.default_language}'")
                self._load_language(self.default_language)
            else:
                raise Exception(f"Default language '{self.default_language}' not found!")
    
    def set_language(self, language: str) -> None:
        """Switch to a different language"""
        self.current_language = language
        self._load_language(language)
    
    def get(self, key: str, **kwargs) -> str:
        """
        Get a text constant by key.
        Supports string formatting with kwargs.
        
        Example:
            texts.get('QUANTITY_LIMIT_EXCEEDED', quantity=5, max_portions=50, current=45)
        """
        text = self._texts.get(key, f"[Missing text: {key}]")
        
        # Support string formatting if kwargs are provided
        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, ValueError):
                return text
        
        return text
    
    def __getattr__(self, key: str) -> str:
        """Allow accessing texts as attributes: texts.WELCOME_TITLE"""
        return self.get(key)
    
    def __getitem__(self, key: str) -> str:
        """Allow accessing texts as dictionary: texts['WELCOME_TITLE']"""
        return self.get(key)
    
    def get_available_languages(self) -> list:
        """Get list of available language files"""
        texts_dir = os.path.dirname(__file__)
        languages = []
        
        for file in os.listdir(texts_dir):
            if file.endswith('.py') and file not in ['__init__.py', 'texts.py']:
                languages.append(file[:-3])  # Remove .py extension
        
        return languages

# Create a global instance for easy importing
texts = TextManager('en')

# Convenience function for quick access
def get_text(key: str, **kwargs) -> str:
    """Convenience function to get text"""
    return texts.get(key, **kwargs)
