import os
from dotenv import load_dotenv

from pathlib import Path

from collection import select_collection
from agent_librarian_dependencies import get_library_shelves
from workflow import workflow


load_dotenv(override=True)
LIBRARY_PATH = Path(os.getenv('LIBRARY_PATH'))

def run(path, library_path):

    collection = select_collection(collection=path, library=library_path)

    for file_path in collection:
        library_shelves = get_library_shelves(path=library_path)

        workflow.run(
            input={
                'library_path': library_path,
                'library_shelves': library_shelves,
                'file_path': file_path
            }
        )