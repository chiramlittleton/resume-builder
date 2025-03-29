from typing import List, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: Literal["contact"] = "contact"
    name: str
    email: str
    phone: str
    website: str

class EducationEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: Literal["education"] = "education"
    name: str  # Human-readable label
    degree: str
    school: str
    years: str

class ExperienceEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: Literal["experience"] = "experience"
    name: str
    title: str
    company: str
    date: str
    bullets: List[str]

class ProjectEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: Literal["project"] = "project"
    name: str  # Project display name
    date: str
    bullets: List[str]
