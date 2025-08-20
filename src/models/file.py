from pydantic import BaseModel
from typing import List

class Dependency(BaseModel):
    file_name: str
    file_path: str

class File(BaseModel):
    file_name: str
    content: str
    exists: bool
    file_path: str
    dependencies: List[Dependency]
