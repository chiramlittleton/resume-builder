from pydantic import BaseModel
from typing import List
from .entries import Contact, EducationEntry, ExperienceEntry, ProjectEntry

class ResumeData(BaseModel):
    template_name: str
    name: str
    contact: Contact
    skills: List[str]
    certificates: List[str]
    education: List[EducationEntry]
    experience: List[ExperienceEntry]
    projects: List[ProjectEntry]
