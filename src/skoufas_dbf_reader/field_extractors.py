from typing import Optional


def has_author(a01: Optional[str]) -> bool:
    """Check values for marks of missing author"""
    if not a01:
        return False
    if a01 in [
        "X . Σ.",
        "X,S",
        "X.S.",
        "X.S",
        "X.Σ.",
        "X.Σ",
        "Χ,Σ",
        "Χ. Σ .",
        "Χ. Σ.",
        "Χ.Σ.",  # greek X
        "Χ.Σ",
        "Χ.Χ.",
        "Χ.Χ",
        "ΧΣ",
    ]:
        return False
    return True


