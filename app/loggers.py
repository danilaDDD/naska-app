import logging
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "app.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

_fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter(_fmt))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(_fmt))

logger = logging.getLogger("naska")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)