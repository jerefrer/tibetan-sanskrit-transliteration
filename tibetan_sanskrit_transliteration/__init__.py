"""
Tibetan Sanskrit Transliteration

A Python library for transliterating Tibetan-encoded Sanskrit mantras to IAST and phonetics.
"""

from .transliterator import TibetanSanskritTransliterator, transliterate

__version__ = "0.1.0"
__all__ = ["TibetanSanskritTransliterator", "transliterate"]
