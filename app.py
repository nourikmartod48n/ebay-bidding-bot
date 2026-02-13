import json
from pathlib import Path
from fastapi import FastAPI, HTTPException

from automation.bid_scheduler import build_plan

app = FastAPI(title="eBay Auction Monitor (Dry-Run)", version="1.0.0")

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
PLAN_FILE = DATA_DIR / "bid_plan.json"
AUCTIONS_FILE = DATA_DIR / "auctions.json"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/auctions")
def auctions():
    if not AUCTIONS_FILE.exists():
        raise HTTPException(status_code=404, detail="data/auctions.json not found")
    return json.loads(AUCTIONS_FILE.read_text(encoding="utf-8"))

@app.post("/plan/rebuild")
def plan_rebuild():
    plan = build_plan()
    return {"count": len(plan), "items": plan}

@app.get("/plan")
def plan():
    if not PLAN_FILE.exists():
        raise HTTPException(status_code=404, detail="data/bid_plan.json not found")
    return json.loads(PLAN_FILE.read_text(encoding="utf-8"))
