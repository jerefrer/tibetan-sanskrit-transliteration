"""
CSV loader for replacement map data.
"""

import csv
import os
from pathlib import Path
from typing import List, Dict, Optional


def load_replacements(csv_path: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Load replacement map from CSV file.
    
    Args:
        csv_path: Path to CSV file. If None, uses bundled data file.
        
    Returns:
        List of dicts with 'tibetan', 'transliteration', 'phonetics' keys.
    """
    if csv_path is None:
        # Default to bundled data file
        csv_path = Path(__file__).parent / "data" / "replacements.csv"
    
    replacements = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            replacements.append({
                'tibetan': row['tibetan'],
                'transliteration': row['transliteration'],
                'phonetics': row.get('phonetics', '') or ''
            })
    
    return replacements
