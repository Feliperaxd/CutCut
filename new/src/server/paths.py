
__all__ = ['Paths']
__author__ = 'Felipe Amaral'
__version__ = '0.2'

from pathlib import Path


class Paths:
    """
    Class that defines paths to various directories in the project.
    Uses direct Path objects for better clarity and maintainability.
    """


    MAIN = Path(__file__).parents[2]
    TEMP = MAIN / 'temp'
    SOURCE = MAIN / 'src'
    CLIENT = SOURCE / 'client'
    SERVER = SOURCE / 'server'
    ASSETS = CLIENT / 'assets'
    SCRIPTS = CLIENT / 'scripts'
    STYLES = CLIENT / 'styles'
    TEMPLATES = CLIENT / 'templates'
    