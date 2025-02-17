
__all__ = ['VideoErrorType']
__author__ = 'Felipe Amaral'
__version__ = '0.1'

from enum import Enum


class VideoErrorType(Enum):
    NOT_VALID = 'not_valid'
    NOT_ALLOWED = 'not_allowed'
    NOT_AVAILABLE = 'not_available'
    UNKNOWN_ERROR = 'unknown_error'
