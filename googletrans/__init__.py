"""Free Google Translate API for Python. Translates totally free of charge."""
__all__ = 'Translator',
__version_info__ = 2, 0, 0
__version__ = '.'.join(str(v) for v in __version_info__)


from googletrans.client import Translator