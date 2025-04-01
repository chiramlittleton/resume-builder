from typing import Union

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Query
from starlette.responses import FileResponse

from backend.db.mongo import db
from backend.models.base import TemplateOnly
from backend.models.entries import Contact, EducationEntry, ExperienceEntry, ProjectEntry
from backend.models.resume import ResumeData
from backend.services.pdf_generator import generate_pdf

router = APIRouter()

@router.post("/generate-resume")
async def generate_resume_from_payload(payload: dict):
    # print(payload)
    pdf_path = generate_pdf(payload)
    return FileResponse(pdf_path, media_type="application/pdf", filename="resume.pdf")

# this code is probably broken
@router.post("/generate-draft-resume")
async def generate_resume_from_draft(draft_name: str = Query(...)):
    draft = await db.drafts.find_one({"draft_name": draft_name})
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    contact = await db.entries.find_one({"name": draft.get("contact_name"), "type": "contact"}) if draft.get("contact_name") else None
    education = await db.entries.find({"name": {"$in": draft.get("education_names", [])}, "type": "education"}).to_list(None)
    experience = await db.entries.find({"name": {"$in": draft.get("experience_names", [])}, "type": "experience"}).to_list(None)
    projects = await db.entries.find({"name": {"$in": draft.get("project_names", [])}, "type": "project"}).to_list(None)

    resume_data = ResumeData(
        template_name=draft["template_name"],
        name=draft["name"],
        contact=Contact(**contact) if contact else Contact(name="",email="", phone="", website=""),
        skills=draft.get("skills", []),
        certificates=draft.get("certificates", []),
        education=[EducationEntry(**e) for e in education],
        experience=[ExperienceEntry(**e) for e in experience],
        projects=[ProjectEntry(**p) for p in projects],
    )

    pdf_path = generate_pdf(resume_data.dict())
    return FileResponse(path=pdf_path, media_type="application/pdf", filename="resume.pdf")
