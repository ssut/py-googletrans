"""Free Google Translate API for Python. Translates totally free of charge."""

__all__ = ("Translator",)
__version__ = "3.0.0"


from pygoogletrans.client import Translator
from pygoogletrans.constants import LANGCODES, LANGUAGES  # noqa
