from typing import List

import hashlib
from pathlib import Path


def checksum(file: Path) -> str:
    md5_hash = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def select_collection(collection: Path, library: Path) -> List[Path]:

    content_library = library.glob(pattern='**/*')
    content_library = [checksum(content) for content in content_library if content.is_file()]

    if collection.is_file():
        content_collection = [collection] if checksum(collection) not in content_library else []
    else:
        content_collection = collection.glob(pattern='**/*')
        content_collection = {checksum(content): content for content in content_collection if content.is_file()}
        content_collection = [path for checksum, path in content_collection.items() if checksum not in content_library]

    for content in content_collection:
        with open(content, 'rb') as file:
            first_bytes = file.read(4)
            if not first_bytes.startswith(b'\x25\x50\x44\x46'): # pdf signature
                content_collection.remove(content)
    
    return content_collection