from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4

class DraftResume(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    draft_name: str
    name: str
    template_name: str
    contact_id: Optional[str] = None
    education_ids: List[str] = []
    experience_ids: List[str] = []
    project_ids: List[str] = []
    skills: List[str] = []
    certificates: List[str] = []
    user_id: Optional[str] = None
