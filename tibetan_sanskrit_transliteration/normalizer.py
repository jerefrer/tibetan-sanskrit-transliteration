"""
Tibetan text normalization utilities.
"""

import re
import unicodedata


def normalize_tibetan(tibetan: str, keep_trailing_tshek: bool = False) -> str:
    """
    Normalize Tibetan text by removing untranscribed punctuation.
    
    Args:
        tibetan: Input Tibetan text
        keep_trailing_tshek: Whether to keep trailing tshek (་)
        
    Returns:
        Normalized Tibetan text
    """
    # Normalize Unicode
    normalized = unicodedata.normalize('NFC', tibetan)
    
    # Normalize combined letters (ported from tibetan-normalizer JS)
    normalized = normalized.replace(' ', ' ')  # Non-breaking space
    normalized = normalized.replace('ༀ', 'ཨོཾ')  # Om symbol
    normalized = normalized.replace('ཀྵ', 'ཀྵ')
    normalized = normalized.replace('བྷ', 'བྷ')
    normalized = re.sub(r'ི+', 'ི', normalized)  # Multiple i vowels
    normalized = re.sub(r'ུ+', 'ུ', normalized)  # Multiple u vowels
    normalized = normalized.replace('ཱུ', 'ཱུ')
    normalized = normalized.replace('ཱི', 'ཱི')
    normalized = normalized.replace('ཱྀ', 'ཱྀ')
    normalized = normalized.replace('དྷ', 'དྷ')
    normalized = normalized.replace('གྷ', 'གྷ')
    normalized = normalized.replace('ཪླ', 'རླ')
    normalized = normalized.replace('ྡྷ', 'ྡྷ')
    
    # Normalize tsheks (ported from tibetan-normalizer JS)
    # Malformed: anusvara before vowel - swap them
    normalized = re.sub(r'(ཾ)([ཱེིོྀུ])', r'\2\1', normalized)
    normalized = normalized.replace('༌', '་')  # Alternative tshek
    normalized = re.sub(r'་+', '་', normalized)  # Multiple consecutive tsheks
    
    # Replace various punctuation with tshek
    normalized = re.sub(r'[༵\u0F04-\u0F0A\u0F0D-\u0F1F\u0F3A-\u0F3F\u0FBE-\uF269]', '་', normalized)
    normalized = normalized.strip()
    
    # Normalize anusvara variants
    normalized = re.sub(r'[ྃྂ]', 'ཾ', normalized)
    
    # Add tshek after certain punctuation
    normalized = re.sub(r'([༔ཿ])', r'\1་', normalized)
    
    # Normalize shad
    normalized = normalized.replace('༌།', '།')
    
    # Handle trailing tshek
    if not keep_trailing_tshek:
        normalized = re.sub(r'་$', '', normalized)
    
    return normalized


def normalize_iast(text: str) -> str:
    """
    Normalize IAST text by removing diacritics for phonetic output.
    
    Args:
        text: IAST text with diacritics
        
    Returns:
        Simplified phonetic text
    """
    # Map of diacritics to simple forms
    replacements = [
        ('ā', 'a'), ('ī', 'i'), ('ū', 'u'),
        ('ṛ', 'ri'), ('ṝ', 'ri'), ('ḷ', 'li'), ('ḹ', 'li'),
        ('ṃ', 'm'), ('ṁ', 'm'), ('ḥ', 'h'),
        ('ṅ', 'ng'), ('ñ', 'ny'),
        ('ṭ', 't'), ('ḍ', 'd'), ('ṇ', 'n'),
        ('ś', 'sh'), ('ṣ', 'sh'),
        ('é', 'e'), ('ē', 'e'),
    ]
    
    result = text
    for old, new in replacements:
        result = result.replace(old, new)
    
    return result
