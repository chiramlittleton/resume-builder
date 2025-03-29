import strawberry
from typing import List, Optional
from backend.db.mongo import db
from backend.api.util import clean_for_gql

@strawberry.type
class Contact:
    id: str
    name: str
    email: str
    phone: str
    website: str

@strawberry.type
class Entry:
    id: str
    type: str
    name: str
    title: Optional[str] = None
    company: Optional[str] = None
    date: Optional[str] = None
    bullets: Optional[List[str]] = None
    degree: Optional[str] = None
    school: Optional[str] = None
    years: Optional[str] = None

@strawberry.type
class Draft:
    draft_name: str
    template_name: str
    name: str
    user_id: Optional[str] = None
    contact_id: Optional[str]
    experience_ids: List[str]
    education_ids: List[str]
    project_ids: List[str]
    skills: List[str]
    certificates: List[str]

    @strawberry.field
    async def experience(self) -> List[Entry]:
        if not self.experience_ids:
            return []
        results = await db.entries.find({"id": {"$in": self.experience_ids}}).to_list(None)
        return [Entry(**e) for e in clean_for_gql(results)]

    @strawberry.field
    async def education(self) -> List[Entry]:
        if not self.education_ids:
            return []
        results = await db.entries.find({"id": {"$in": self.education_ids}}).to_list(None)
        return [Entry(**e) for e in clean_for_gql(results)]

    @strawberry.field
    async def projects(self) -> List[Entry]:
        if not self.project_ids:
            return []
        results = await db.entries.find({"id": {"$in": self.project_ids}}).to_list(None)
        return [Entry(**p) for p in clean_for_gql(results)]

    @strawberry.field
    async def contact(self) -> Optional[Contact]:
        if self.contact_id:
            doc = await db.entries.find_one({"id": self.contact_id, "type": "contact"})
            if doc:
                return Contact(**clean_for_gql(doc))
        return None

@strawberry.type
class Query:
    @strawberry.field
    async def drafts(self) -> List[Draft]:
        drafts = await db.drafts.find().to_list(None)
        return [Draft(**d) for d in clean_for_gql(drafts)]

    @strawberry.field
    async def entries(self, type: str) -> List[Entry]:
        entries = await db.entries.find({"type": type}).to_list(None)
        return [Entry(**e) for e in clean_for_gql(entries)]

schema = strawberry.Schema(query=Query)
