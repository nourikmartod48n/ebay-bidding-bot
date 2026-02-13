from typing import Any, Dict, List

def require_keys(obj: Dict[str, Any], keys: List[str]) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

def as_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default

def as_int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except Exception:
        return default
