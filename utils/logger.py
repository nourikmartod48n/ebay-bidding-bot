import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(name: str = "ebay_bidding_automation") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    exec_handler = RotatingFileHandler(LOG_DIR / "execution.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8")
    exec_handler.setLevel(logging.INFO)
    exec_handler.setFormatter(fmt)

    err_handler = RotatingFileHandler(LOG_DIR / "error.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8")
    err_handler.setLevel(logging.WARNING)
    err_handler.setFormatter(fmt)

    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    stream.setFormatter(fmt)

    logger.addHandler(exec_handler)
    logger.addHandler(err_handler)
    logger.addHandler(stream)
    return logger
