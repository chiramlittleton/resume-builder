from fastapi import APIRouter
from app.models.schemas import Entry
from app.db.mongo import db

router = APIRouter()

@router.post("/generate-resume")
def generate_resume(payload: Union[ResumeData, TemplateOnly] = Body(...)):
    data = payload.dict()
    pdf_path = generate_pdf(data)
    return FileResponse(path=pdf_path, media_type="application/pdf", filename="resume.pdf")

@router.post("/generate-draft-resume")
async def generate_resume_from_draft(draft_id: str = Query(...)):
    draft = await db.drafts.find_one({"_id": ObjectId(draft_id)})
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
