from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from utils.validators import as_float, as_int

@dataclass
class StrategyConfig:
    max_bid: float
    bid_window_seconds: int
    min_increment: float
    dry_run: bool = True

def should_schedule_bid(auction: Dict[str, Any], now_epoch: int, cfg: StrategyConfig) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Decide whether to schedule a bid in the final window.

    Returns: (should_schedule, plan_dict)
    plan_dict includes a recommended bid amount and schedule time.

    Note: This repo does not execute live bids.
    """
    end_time = as_int(auction.get("end_time_epoch"), 0)
    remaining = end_time - now_epoch
    if remaining <= 0:
        return False, None

    if remaining > cfg.bid_window_seconds:
        return False, None

    price = as_float(auction.get("current_price"), 0.0)
    recommended = price + cfg.min_increment
    if recommended > cfg.max_bid:
        return False, None

    plan = {
        "auction_id": auction.get("auction_id"),
        "title": auction.get("title"),
        "current_price": price,
        "recommended_bid": round(recommended, 2),
        "schedule_at_epoch": max(now_epoch, end_time - 3),  # aim ~3s before end
        "dry_run": cfg.dry_run,
        "reason": "within_bid_window",
    }
    return True, plan
