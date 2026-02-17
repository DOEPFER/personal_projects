from typing import Dict, List
from pydantic import BaseModel, Field

class LibrarianInput(BaseModel):
    metadata: Dict[str, str] = Field(description='Document metadata such as title, author, and subject.')
    sample: str = Field(description='A sample of the document content to help the agent understand the document.')
    library_shelves: List[str] = Field(description='The folders currently existing in the library.')

class LibrarianOutput(BaseModel):
    file_name: str = Field(description='The name generated for the analyzed file.')
    file_path: str = Field(description='The folder (shelf) chosen for the analyzed file.')
    summary: str = Field(description='A summary of the document content.')
    tags: List[str] = Field(description='Tags to help classify the document.')