from pathlib import Path

from datetime import datetime, timezone
import logging
import time
import sys

from logging import Logger

def setup_logging(logprefix: str = 'mirror', verbose: bool = False) -> Logger:
    log_dir = Path('log')
    log_dir.mkdir(parents=True, exist_ok=True)

    date = datetime.now(timezone.utc)
    log_filename = f'{logprefix}_{date:%Y_%m_%d}.log'
    log_file_path = log_dir / log_filename

    handlers = [logging.FileHandler(log_file_path, encoding='utf-8'), logging.StreamHandler(sys.stdout)] if verbose else [logging.FileHandler(log_file_path, encoding='utf-8')]

    logging.Formatter.converter = time.gmtime # UTC

    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)sZ | %(levelname)s | [%(name)s] | %(message)s',
        handlers=handlers, # type: ignore
        datefmt='%Y-%m-%dT%H:%M:%S' # ISO 8601
    )

    return logging.getLogger('mirror')