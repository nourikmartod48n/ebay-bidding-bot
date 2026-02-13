import json
from pathlib import Path
from typing import Any, Dict, List

from utils.logger import setup_logger
from utils.validators import require_keys

logger = setup_logger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)
AUCTIONS_FILE = DATA_DIR / "auctions.json"

def load_auctions() -> List[Dict[str, Any]]:
    if not AUCTIONS_FILE.exists():
        return []
    return json.loads(AUCTIONS_FILE.read_text(encoding="utf-8"))

def save_auctions(auctions: List[Dict[str, Any]]) -> None:
    AUCTIONS_FILE.write_text(json.dumps(auctions, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Saved %s auction snapshots to %s", len(auctions), AUCTIONS_FILE)

def validate_auction(a: Dict[str, Any]) -> None:
    # Minimal schema for strategy/scheduler.
    require_keys(a, ["auction_id", "title", "current_price", "end_time_epoch"])
