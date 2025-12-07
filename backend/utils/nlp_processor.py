# backend/utils/nlp_processor.py
# Lightweight NLP helper — NO spaCy required.
# Uses simple regex and basic Python string ops to clean text and extract tokens.
import re
from typing import List, Dict

def clean_text(text: str) -> str:
    if not text:
        return ''
    # basic cleaning: normalize whitespace and remove repeated newlines
    t = text.replace('\r\n', '\n').replace('\r', '\n')
    t = re.sub(r'\n\s+', '\n', t)
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def extract_sentences(text: str) -> List[str]:
    t = clean_text(text)
    # naive sentence split on punctuation followed by space/newline
    sentences = re.split(r'(?<=[\.\?\!])\s+', t)
    return [s.strip() for s in sentences if s.strip()]

def find_medical_terms(text: str, keywords: List[str]) -> Dict[str, int]:
    """
    Return counts of keyword matches (case-insensitive).
    Used as a simple fallback to identify presence of terms.
    """
    t = text.lower()
    out = {}
    for k in keywords:
        out[k] = len(re.findall(re.escape(k.lower()), t))
    return out

def extract_test_values(text: str):
    """
    Very permissive regex-based extractor for patterns like:
    **HbA1c**: 5.9 %
    HbA1c: 5.9 %
    HbA1c - 5.9%
    Returns list of dicts: [{'name':..., 'value':..., 'unit':...}, ...]
    """
    if not text:
        return []
    patterns = [
        r"\*\*([A-Za-z0-9\s\-/()]+?)\*\*[:\-]\s*([\d]+(?:\.\d+)?)\s*([a-zA-Z/%]+)?",
        r"([A-Za-z0-9\s\-/()]+?)[:\-]\s*([\d]+(?:\.\d+)?)\s*([a-zA-Z/%]+)"
    ]
    results = []
    for pat in patterns:
        for m in re.finditer(pat, text):
            name = m.group(1).strip()
            value = float(m.group(2))
            unit = m.group(3).strip() if m.group(3) else ''
            results.append({'name': name, 'value': value, 'unit': unit})
    # dedupe by name keeping first occurrences in order of appearance
    seen = {}
    dedup = []
    for r in results:
        key = r['name'].lower()
        if key not in seen:
            seen[key] = True
            dedup.append(r)
    return dedup
