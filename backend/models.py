from beanie import Document
from typing import List
from pydantic import BaseModel

class ExperienceEntry(BaseModel):
    company: str
    role: str
    date: str
    bullets: List[str]

class Resume(Document):
    name: str
    email: str
    phone: str
    experience: List[ExperienceEntry]
