# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from dataclasses import dataclass, field
# ******************************OWN LIBRARIES*********************************

# ****************************************************************************
@dataclass
class Book:
    _id: str
    name: str
    author: str
    year: int = 0
    original_language: str = ""
    description: str = ""
    
@dataclass
class Note:
    _id: str
    bookID: str
    name: str
    author: str
    notes: list
