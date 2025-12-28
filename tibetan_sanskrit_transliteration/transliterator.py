"""
Main transliterator class for Tibetan Sanskrit to IAST/phonetics conversion.
"""

import re
from typing import Optional, Literal

from tibetan_sanskrit_transliteration_data import load_replacements
from .normalizer import normalize_tibetan, normalize_iast


class TibetanSanskritTransliterator:
    """
    Transliterates Tibetan-encoded Sanskrit mantras to IAST or phonetics.
    """
    
    # Tibetan vowel markers that override the inherent 'a'
    VOWEL_MARKERS = '\u0f71\u0f72\u0f74\u0f7a\u0f7c\u0f7e\u0f80'
    
    def __init__(self):
        """
        Initialize the transliterator.
        """
        raw_replacements = load_replacements()
        # Preprocess Tibetan patterns and pre-compile regex
        self.replacements = []
        for entry in raw_replacements:
            tibetan = normalize_tibetan(entry['tibetan'])
            if not tibetan:
                continue
            
            transliteration = entry['transliteration']
            phonetics = entry['phonetics']
            
            # Pre-compile regex patterns for performance
            try:
                base_re = re.compile(tibetan)
                # Pre-compile suffix patterns too
                tshek_re = re.compile(f"{tibetan}[་།༑༔]")
                visarga_re = re.compile(f"{tibetan}ཿ")
                vowel_re = re.compile(f"{tibetan}([{self.VOWEL_MARKERS}])")
            except re.error:
                # Pattern is not valid regex, use string replacement
                base_re = None
                tshek_re = None
                visarga_re = None
                vowel_re = None
            
            self.replacements.append({
                'tibetan': tibetan,
                'transliteration': transliteration,
                'phonetics': phonetics,
                'regex': base_re,
                'tshek_re': tshek_re,
                'visarga_re': visarga_re,
                'vowel_re': vowel_re,
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
        
        for word in self.replacements:
            if mode == 'phonetics':
                replacement = word['phonetics'] or normalize_iast(word['transliteration'])
            else:
                replacement = word['transliteration']
            
            pattern = word['tibetan']
            compiled_re = word['regex']
            
            # Use pre-compiled regex if available, otherwise string replace
            if compiled_re is None:
                replaced = replaced.replace(pattern, replacement)
                continue
            
            # Handle words ending in 'a' - special suffix handling
            if replacement.endswith('a') and word['tshek_re']:
                base = replacement[:-1]
                
                # Handle word-final with tshek/shad
                replaced = word['tshek_re'].sub(f"{replacement} ", replaced)
                
                # Handle visarga
                replaced = word['visarga_re'].sub(f"{base}{'ah' if mode == 'phonetics' else 'aḥ'}", replaced)
                
                # For consonants followed by vowel markers, replace with base (no 'a')
                replaced = word['vowel_re'].sub(f"{base}\\1", replaced)
            
            # General replacement for remaining occurrences
            replaced = compiled_re.sub(replacement, replaced)
        
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


# Singleton instance for repeated use
_default_transliterator: Optional[TibetanSanskritTransliterator] = None


def get_transliterator() -> TibetanSanskritTransliterator:
    """
    Get or create a singleton transliterator instance.
        
    Returns:
        TibetanSanskritTransliterator instance
    """
    global _default_transliterator
    if _default_transliterator is None:
        _default_transliterator = TibetanSanskritTransliterator()
    return _default_transliterator


def transliterate(
    tibetan: str,
    mode: Literal['iast', 'phonetics'] = 'iast',
    capitalize: bool = False,
    anusvara_style: Literal['ṃ', 'ṁ'] = 'ṃ'
) -> str:
    """
    Convenience function to transliterate Tibetan Sanskrit text.
    
    Uses a cached singleton instance for performance.
    
    Args:
        tibetan: Input Tibetan text
        mode: Output mode - 'iast' or 'phonetics'
        capitalize: Whether to capitalize first letter of each group
        anusvara_style: Anusvara character to use ('ṃ' or 'ṁ')
        
    Returns:
        Transliterated text
    """
    return get_transliterator().transliterate(tibetan, mode, capitalize, anusvara_style)
