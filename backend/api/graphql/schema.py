from __future__ import annotations

import strawberry
from typing import List, Optional, Union
from backend.db.mongo import db
from backend.api.util import clean_for_gql


# === ENTRY TYPES ===

@strawberry.type
class ContactEntry:
    id: str
    type: str = "contact"
    name: str
    location: str
    phone: str
    email: str
    website: Optional[str]
    github: Optional[str]
    linkedin: Optional[str]


@strawberry.type
class SummaryEntry:
    id: str
    type: str = "summary"
    text: str


@strawberry.type
class SkillsGroup:
    name: str
    items: List[str]


@strawberry.type
class SkillsEntry:
    id: str
    type: str = "skills"
    groups: List[SkillsGroup]


@strawberry.type
class ExperienceEntry:
    id: str
    type: str = "experience"
    title: str
    organization: str
    location: str
    dateRange: str
    bulletPoints: List[str]
    technologies: List[str]


@strawberry.type
class ProjectEntry:
    id: str
    type: str = "project"
    name: str
    url: Optional[str]
    description: str
    technologies: List[str]


@strawberry.type
class Education:
    school: str
    degree: str


@strawberry.type
class EducationCertEntry:
    id: str
    type: str = "educationCerts"
    education: List[Education]
    certifications: List[str]


@strawberry.type
class KeywordsEntry:
    id: str
    type: str = "keywords"
    items: List[str]


# === UNION TYPE ===

Entry = strawberry.union(
    "Entry",
    (
        ContactEntry,
        SummaryEntry,
        SkillsEntry,
        ExperienceEntry,
        ProjectEntry,
        EducationCertEntry,
        KeywordsEntry,
    ),
)


# === DRAFT ===

@strawberry.type
class Draft:
    id: str
    name: str
    templateName: str
    entries: List[Entry]


# === QUERY ===

@strawberry.type
class Query:
    @strawberry.field
    async def drafts(self) -> List[Draft]:
        raw_drafts = await db.drafts.find().to_list(None)
        raw_entries = await db.entries.find().to_list(None)

        draft_map = {d["id"]: d for d in clean_for_gql(raw_drafts)}
        entry_map = {e["id"]: e for e in clean_for_gql(raw_entries)}

        result = []
        for draft_id, draft in draft_map.items():
            entry_ids = draft.get("entries", [])
            typed_entries = []
            for entry_id in entry_ids:
                raw_entry = entry_map.get(entry_id)
                if raw_entry:
                    try:
                        typed_entries.append(parse_entry(raw_entry))
                    except Exception as e:
                        print(f"Failed to parse entry {entry_id}: {e}")
            result.append(
                Draft(
                    id=draft_id,
                    name=draft["name"],
                    templateName=draft["templateName"],
                    entries=typed_entries,
                )
            )

        return result


# === ENTRY FACTORY ===

def parse_entry(entry: dict) -> Entry:
    t = entry.get("type")
    if t == "summary":
        return SummaryEntry(**entry)
    if t == "skills":
        # hydrate nested objects
        groups = [SkillsGroup(**g) for g in entry["groups"]]
        return SkillsEntry(id=entry["id"], type=entry["type"], groups=groups)
    if t == "experience":
        return ExperienceEntry(**entry)
    if t == "project":
        return ProjectEntry(**entry)
    if t == "educationCerts":
        education = [Education(**e) for e in entry["education"]]
        return EducationCertEntry(
            id=entry["id"],
            type=entry["type"],
            education=education,
            certifications=entry["certifications"],
        )
    if t == "keywords":
        return KeywordsEntry(**entry)
    if t == "contact":
        required_fields = ["id", "name", "location", "phone", "email"]
        for field in required_fields:
            if field not in entry:
                raise ValueError(f"Missing required field '{field}' in contact entry: {entry}")
        return ContactEntry(**entry)
    raise ValueError(f"Unsupported entry type: {t}")


# === SCHEMA ===

schema = strawberry.Schema(query=Query)
