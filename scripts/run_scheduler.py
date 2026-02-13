from automation.bid_scheduler import build_plan, run_dry_scheduler

def main():
    plan = build_plan()
    run_dry_scheduler(plan)

if __name__ == "__main__":
    main()
