# eBay Bidding Automation (Monitoring + Dry-Run)

> **Important:** This repository intentionally does **not** place live bids.
> Automating bidding may violate marketplace rules and can create unfair or abusive behaviour.
> This project focuses on **auction monitoring**, **strategy simulation**, and a **dry-run scheduler**
> that produces a clear, auditable “bid plan” for manual execution.

It addresses the operational intent behind searches like *ebay bidding bot*, *bidding bot for eBay*,
*ebay bid bot*, and *bidding bots ebay* by providing a production-grade toolkit for
timing analysis and rule-based decisions—without submitting bids.

## What it does

- Syncs auction snapshots into `data/auctions.json` (from an input list)
- Runs a rule-based strategy to decide if/when a bid should be scheduled
- Writes a **bid plan** and **bid log** to JSON for review
- Exposes a small FastAPI service for health checks and plan inspection

## Quick Start

    pip install -r requirements.txt
    python scripts/sync_auctions.py
    python scripts/run_scheduler.py

## Live bidding

If you need live bidding, integrate the official eBay APIs yourself, ensure compliance with eBay policies,
and keep manual confirmation in the loop.
