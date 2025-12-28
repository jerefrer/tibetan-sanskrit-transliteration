"""
Main transliterator class for Tibetan Sanskrit to IAST/phonetics conversion.
"""

import re
from typing import Optional, Literal

from .loader import load_replacements
from .normalizer import normalize_tibetan, normalize_iast


class TibetanSanskritTransliterator:
    """
    Transliterates Tibetan-encoded Sanskrit mantras to IAST or phonetics.
    """
    
    def __init__(self, csv_path: Optional[str] = None):
        """
        Initialize the transliterator.
        
        Args:
            csv_path: Optional path to custom replacements CSV file.
        """
        raw_replacements = load_replacements(csv_path)
        # Preprocess Tibetan patterns
        self.replacements = []
        for entry in raw_replacements:
            self.replacements.append({
                'tibetan': normalize_tibetan(entry['tibetan']),
                'transliteration': entry['transliteration'],
                'phonetics': entry['phonetics']
            })
    
    def transliterate(
        self,
        tibetan: str,
        mode: Literal['iast', 'phonetics'] = 'iast',
        capitalize: bool = False,
        anusvara_style: Literal['ṃ', 'ṁ'] = 'ṃ'
    ) -> str:
        """
        Transliterate Tibetan Sanskrit text.
        
        Args:
            tibetan: Input Tibetan text
            mode: Output mode - 'iast' or 'phonetics'
            capitalize: Whether to capitalize first letter of each group
            anusvara_style: Anusvara character to use ('ṃ' or 'ṁ')
            
        Returns:
            Transliterated text
        """
        replaced = normalize_tibetan(tibetan, keep_trailing_tshek=True)
        
        # Tibetan vowel markers that override the inherent 'a'
        # U+0F71 (ཱ), U+0F72 (ི), U+0F74 (ུ), U+0F7A (ེ), U+0F7C (ོ), U+0F7E (ཾ), U+0F80 (ྀ)
        vowel_markers = '\u0f71\u0f72\u0f74\u0f7a\u0f7c\u0f7e\u0f80'
        
        for word in self.replacements:
            if mode == 'phonetics':
                replacement = word['phonetics'] or normalize_iast(word['transliteration'])
            else:
                replacement = word['transliteration']
            
            pattern = word['tibetan']
            
            # Skip empty patterns
            if not pattern:
                continue
            
            # Handle -nāṃ suffix
            try:
                replaced = re.sub(
                    f"({pattern}[^་།༑༔]*)་ནཱཾ",
                    f"\\1་^^^{'nam' if mode == 'phonetics' else 'nāṃ'}",
                    replaced
                )
            except re.error:
                pass
            
            # Handle words ending in 'a' - the 'a' is only added when followed by tshek/shad
            # If followed by a vowel marker, the vowel marker will be processed separately
            if replacement.endswith('a'):
                base = replacement[:-1]
                
                try:
                    # Handle word-final with tshek/shad - replace with full replacement + space
                    replaced = re.sub(
                        f"{pattern}[་།༑༔]",
                        f"{replacement} ",
                        replaced
                    )
                    
                    # Handle visarga
                    replaced = re.sub(
                        f"{pattern}ཿ",
                        f"{base}{'ah' if mode == 'phonetics' else 'aḥ'}",
                        replaced
                    )
                    
                    # For consonants followed by vowel markers, replace with base (no 'a')
                    # The vowel marker will be processed later
                    replaced = re.sub(
                        f"{pattern}([{vowel_markers}])",
                        f"{base}\\1",
                        replaced
                    )
                except re.error:
                    pass
            
            # General replacement for remaining occurrences
            try:
                replaced = re.sub(pattern, replacement, replaced)
            except re.error:
                # If regex fails, try literal replacement
                replaced = replaced.replace(pattern, replacement)
        
        # Replace tshek with space and clean up markers
        result = replaced.replace('་', ' ')
        result = re.sub(r' ?\^\^\^', '', result)
        
        # Fix double vowel issues from overlapping replacements
        # e.g., 'aā' -> 'ā', 'aī' -> 'ī', etc.
        result = re.sub(r'a([āīūṛṝḷḹ])', r'\1', result)
        result = re.sub(r'a([ṃṁ])', r'\1', result)  # aṃ -> ṃ when preceded by vowel
        
        # Handle capitalization
        if capitalize:
            result = result[0].upper() + result[1:] if result else result
            result = re.sub(r' {2,}(.)', lambda m: '    ' + m.group(1).upper(), result)
        else:
            result = re.sub(r' {2,}', '    ', result)
        
        # Apply anusvara style
        if anusvara_style == 'ṁ':
            result = result.replace('ṃ', 'ṁ')
        
        return result.strip()


def transliterate(
    tibetan: str,
    mode: Literal['iast', 'phonetics'] = 'iast',
    capitalize: bool = False,
    anusvara_style: Literal['ṃ', 'ṁ'] = 'ṃ',
    csv_path: Optional[str] = None
) -> str:
    """
    Convenience function to transliterate Tibetan Sanskrit text.
    
    Args:
        tibetan: Input Tibetan text
        mode: Output mode - 'iast' or 'phonetics'
        capitalize: Whether to capitalize first letter of each group
        anusvara_style: Anusvara character to use ('ṃ' or 'ṁ')
        csv_path: Optional path to custom replacements CSV file
        
    Returns:
        Transliterated text
    """
    transliterator = TibetanSanskritTransliterator(csv_path)
    return transliterator.transliterate(tibetan, mode, capitalize, anusvara_style)


# Singleton instance for repeated use
_default_transliterator: Optional[TibetanSanskritTransliterator] = None


def get_transliterator(csv_path: Optional[str] = None) -> TibetanSanskritTransliterator:
    """
    Get or create a singleton transliterator instance.
    
    Args:
        csv_path: Optional path to custom replacements CSV file
        
    Returns:
        TibetanSanskritTransliterator instance
    """
    global _default_transliterator
    if _default_transliterator is None:
        _default_transliterator = TibetanSanskritTransliterator(csv_path)
    return _default_transliterator
