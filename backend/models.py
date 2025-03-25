from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from uuid import uuid4

# --- Template-only preview ---
class TemplateOnly(BaseModel):
    template_name: str

# --- Modular entries ---
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

# --- Full resume structure (used for rendering only) ---
class ResumeData(BaseModel):
    template_name: str
    name: str
    contact: Contact
    skills: List[str]
    certificates: List[str]
    education: List[EducationEntry]
    experience: List[ExperienceEntry]
    projects: List[ProjectEntry]

# --- Draft resume structure (used for storage and editing) ---
class DraftResume(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    draft_name: str  # Display name for UI
    name: str
    template_name: str
    contact_id: Optional[str] = None
    education_ids: List[str] = []
    experience_ids: List[str] = []
    project_ids: List[str] = []
    skills: List[str] = []
    certificates: List[str] = []
    user_id: Optional[str] = None  # Optional user scoping
