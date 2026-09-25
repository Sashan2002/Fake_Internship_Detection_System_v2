"""
Assembles a combined text field for NLP input from an advertisement
record, using the SAME normalisation as the ml/ training pipeline
(ml/preprocessing/clean_text.py) to avoid train/serve skew - directly
ported from backend/utils/preprocessing.py in the Flask build.
"""
from ml.preprocessing.clean_text import minimal_normalise


def build_combined_text(record: dict) -> str:
    parts = [
        record.get("title") or "",
        record.get("company_profile") or "",
        record.get("description") or "",
        record.get("requirements") or "",
        record.get("benefits") or "",
    ]
    combined = " ".join(p for p in parts if p)
    return minimal_normalise(combined)
