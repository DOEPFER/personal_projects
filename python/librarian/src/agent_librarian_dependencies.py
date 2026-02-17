from typing import List

from pathlib import Path

def get_library_shelves(path: Path) -> List[str]:
    return [shelf.relative_to(path).as_posix() for shelf in path.rglob(pattern='*/')]