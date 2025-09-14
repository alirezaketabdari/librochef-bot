# Constants package initialization
# Easy imports for constants and variables

from . import variables
from .variables import *
from .texts import texts, get_text, TextManager

# Make it easy to import everything
__all__ = ['texts', 'get_text', 'TextManager'] + variables.__all__
