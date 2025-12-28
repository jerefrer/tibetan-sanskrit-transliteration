# Tibetan Sanskrit Transliteration (Python)

A Python library for transliterating Tibetan-encoded Sanskrit mantras to IAST and phonetics.

## Installation

```bash
pip install tibetan-sanskrit-transliteration
```

Or install from source:

```bash
pip install -e .
```

## Usage

### Basic Usage

```python
from tibetan_sanskrit_transliteration import transliterate

# Transliterate to IAST (default)
tibetan = "ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།"
result = transliterate(tibetan)
print(result)  # "oṃ maṇi padmé hūṃ"

# Transliterate to phonetics
result = transliterate(tibetan, mode='phonetics')
print(result)  # "om mani padme hung"
```

### Options

```python
from tibetan_sanskrit_transliteration import transliterate

result = transliterate(
    tibetan,
    mode='iast',           # 'iast' or 'phonetics'
    capitalize=True,       # Capitalize first letter of each group
    anusvara_style='ṁ'     # 'ṃ' (default) or 'ṁ'
)
```

### Using the Class

For repeated transliterations, use the class to avoid reloading the CSV:

```python
from tibetan_sanskrit_transliteration import TibetanSanskritTransliterator

transliterator = TibetanSanskritTransliterator()

result1 = transliterator.transliterate("ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།")
result2 = transliterator.transliterate("ཨོཾ་ཨཱཿཧཱུྃ།")
```

### Custom Replacement Data

You can provide your own CSV file with replacement rules:

```python
from tibetan_sanskrit_transliteration import TibetanSanskritTransliterator

transliterator = TibetanSanskritTransliterator(csv_path='/path/to/custom.csv')
```

## Data Format

The replacement CSV file has three columns:

| Column            | Description                                 |
| ----------------- | ------------------------------------------- |
| `tibetan`         | Tibetan Unicode pattern (may include regex) |
| `transliteration` | IAST transliteration output                 |
| `phonetics`       | Phonetic output (optional)                  |

## License

MIT License - Copyright Padmakara, 2021-present.
