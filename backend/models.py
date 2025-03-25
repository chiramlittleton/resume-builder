from pydantic import BaseModel
from typing import List

class TemplateOnly(BaseModel):
    template_name: str

class Contact(BaseModel):
    email: str
    phone: str
    website: str

class EducationEntry(BaseModel):
    degree: str
    school: str
    years: str

class ExperienceEntry(BaseModel):
    title: str
    company: str
    date: str
    bullets: List[str]

class ProjectEntry(BaseModel):
    name: str
    date: str
    bullets: List[str]

class ResumeData(BaseModel):
    template_name: str  
    name: str
    contact: Contact
    skills: List[str]
    certificates: List[str]
    education: List[EducationEntry]
    experience: List[ExperienceEntry]
    projects: List[ProjectEntry]
