import json
import time
from pathlib import Path
from typing import Any, Dict, List

import yaml

from automation.auction_monitor import load_auctions, validate_auction
from automation.bid_strategy import StrategyConfig, should_schedule_bid
from utils.logger import setup_logger
from utils.validators import as_int

logger = setup_logger(__name__)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
BID_LOG_FILE = DATA_DIR / "bid_log.json"
BID_PLAN_FILE = DATA_DIR / "bid_plan.json"

RULES_FILE = ROOT / "config" / "auction_rules.yaml"

def _append_log(entry: Dict[str, Any]) -> None:
    existing: List[Dict[str, Any]] = []
    if BID_LOG_FILE.exists():
        existing = json.loads(BID_LOG_FILE.read_text(encoding="utf-8"))
    existing.append(entry)
    BID_LOG_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")

def build_plan() -> List[Dict[str, Any]]:
    cfg_raw = yaml.safe_load(RULES_FILE.read_text(encoding="utf-8"))["defaults"]
    cfg = StrategyConfig(
        max_bid=float(cfg_raw["max_bid"]),
        bid_window_seconds=int(cfg_raw["bid_window_seconds"]),
        min_increment=float(cfg_raw["min_increment"]),
        dry_run=bool(cfg_raw.get("dry_run", True)),
    )

    auctions = load_auctions()
    now = int(time.time())
    plan: List[Dict[str, Any]] = []

    for a in auctions:
        try:
            validate_auction(a)
            ok, item = should_schedule_bid(a, now_epoch=now, cfg=cfg)
            _append_log({
                "ts_epoch": now,
                "auction_id": a.get("auction_id"),
                "decision": "schedule" if ok else "skip",
                "current_price": a.get("current_price"),
            })
            if ok and item:
                plan.append(item)
        except Exception as e:
            _append_log({
                "ts_epoch": now,
                "auction_id": a.get("auction_id"),
                "decision": "error",
                "error": str(e),
            })

    BID_PLAN_FILE.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Built bid plan with %s items at %s", len(plan), BID_PLAN_FILE)
    return plan

def run_dry_scheduler(plan: List[Dict[str, Any]]) -> None:
    """Simulate waiting until schedule times and then logging 'READY' events."""
    for item in sorted(plan, key=lambda x: as_int(x.get("schedule_at_epoch"), 0)):
        target = as_int(item.get("schedule_at_epoch"), 0)
        now = int(time.time())
        if target > now:
            time.sleep(min(target - now, 5))  # short sleep cap for demo
        logger.info("DRY-RUN READY: auction_id=%s recommended_bid=%s title=%s",
                    item.get("auction_id"), item.get("recommended_bid"), item.get("title"))
