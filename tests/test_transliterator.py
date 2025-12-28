"""
Tests for the Tibetan Sanskrit transliterator.
"""

import pytest
from tibetan_sanskrit_transliteration import transliterate, TibetanSanskritTransliterator


class TestTransliterate:
    """Test the transliterate function."""
    
    def test_basic_iast(self):
        """Test basic IAST transliteration."""
        result = transliterate("ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།")
        assert result == "oṃ maṇi padmé hūṃ"
    
    def test_basic_phonetics(self):
        """Test basic phonetics transliteration."""
        result = transliterate("ཨོཾ་ཨ་ར་པ་ཙ་ན།", mode='phonetics')
        assert result == "om a ra pa cha na"
    
    def test_anusvara_style_default(self):
        """Test default anusvara style (ṃ)."""
        result = transliterate("ཨོཾ་ཨཱཿཧཱུྃ།")
        assert "ṃ" in result
        assert "ṁ" not in result
    
    def test_anusvara_style_alternate(self):
        """Test alternate anusvara style (ṁ)."""
        result = transliterate("ཨོཾ་ཨཱཿཧཱུྃ།", anusvara_style='ṁ')
        assert "ṁ" in result
        assert "ṃ" not in result
    
    def test_capitalize(self):
        """Test capitalization."""
        result = transliterate("ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།", capitalize=True)
        assert result[0].isupper()


class TestTransliteratorClass:
    """Test the TibetanSanskritTransliterator class."""
    
    def test_reuse(self):
        """Test that the class can be reused for multiple transliterations."""
        t = TibetanSanskritTransliterator()
        result1 = t.transliterate("ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།")
        result2 = t.transliterate("ཨོཾ་ཨཱཿཧཱུྃ།")
        assert result1 == "oṃ maṇi padmé hūṃ"
        assert result2 == "oṃ āḥ hūṃ"


# Test cases from the JS tests
iast_test_cases = [
    ("ཨོཾ་ཨཱཿཧཱུྃ།", "oṃ āḥ hūṃ"),
    ("ཨོཾ་ཨཱཿཧཱུྃ་སྭཱ་ཧཱ།", "oṃ āḥ hūṃ svāhā"),
    ("ཨོཾ་ཧཱུྃ་ཏྲཱཾ་ཧྲཱིཿཨཱཿ", "oṃ hūṃ trāṃ hrīḥ āḥ"),
    ("འཿཨཿཧཿཤཿསཿམཿ", "āḥ aḥ haḥ śaḥ saḥ maḥ"),
    ("ཨོཾ་བཛྲ་སཏྭ་ཧཱུྃ།", "oṃ vajra satva hūṃ"),
    ("ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།", "oṃ maṇi padmé hūṃ"),
    ("ཨོཾ་ཏཱ་རེ་ཏུཏྟཱ་རེ་ཏུ་རེ་སྭཱ་ཧཱ།", "oṃ tāré tuttāré turé svāhā"),
]


@pytest.mark.parametrize("tibetan,expected", iast_test_cases)
def test_iast_cases(tibetan, expected):
    """Test IAST transliteration cases."""
    result = transliterate(tibetan)
    assert result == expected


phonetics_test_cases = [
    ("ཨོཾ་ཨ་ར་པ་ཙ་ན།", "om a ra pa cha na"),
    ("བཛྲ་པཱ་ཙ་ཧོ།", "vajra pacha ho"),
]


@pytest.mark.parametrize("tibetan,expected", phonetics_test_cases)
def test_phonetics_cases(tibetan, expected):
    """Test phonetics transliteration cases."""
    result = transliterate(tibetan, mode='phonetics')
    assert result == expected
