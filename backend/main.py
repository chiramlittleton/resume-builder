from fastapi import FastAPI, HTTPException, Body, Query, Path
from typing import Union, List
from bson import ObjectId
from bson.errors import InvalidId
from fastapi.responses import FileResponse
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from models import ResumeData, TemplateOnly, DraftResume, Contact, ExperienceEntry, EducationEntry, ProjectEntry
from generate import generate_pdf
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.resume_db

@app.post("/generate-resume")
def generate_resume(payload: Union[ResumeData, TemplateOnly] = Body(...)):
    data = payload.dict()
    pdf_path = generate_pdf(data)
    return FileResponse(path=pdf_path, media_type="application/pdf", filename="resume.pdf")

@app.post("/generate-draft-resume")
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

def clean_mongo_doc(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])  # Or use `del doc["_id"]` to remove it entirely
    return doc

# === Entry CRUD Endpoints ===

@app.post("/entries/", response_model=dict)
async def create_entry(entry: dict):
    result = await db.entries.insert_one(entry)
    entry["_id"] = str(result.inserted_id)
    return entry

@app.get("/entries/{entry_type}", response_model=List[dict])
async def get_entries(entry_type: str):
    entries = await db.entries.find({"type": entry_type}).to_list(length=None)
    return [clean_mongo_doc(e) for e in entries]

@app.get("/entries/{entry_type}/{entry_id}", response_model=dict)
async def get_entry(entry_type: str, entry_id: str):
    entry = await db.entries.find_one({"id": entry_id, "type": entry_type})
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@app.put("/entries/{entry_type}/{entry_id}", response_model=dict)
async def update_entry(entry_type: str, entry_id: str, data: dict = Body(...)):
    result = await db.entries.find_one_and_update(
        {"id": entry_id, "type": entry_type}, {"$set": data}, return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Entry not found")
    return clean_mongo_doc(result)

@app.delete("/entries/{entry_type}/{entry_id}", response_model=dict)
async def delete_entry(entry_type: str, entry_id: str):
    result = await db.entries.delete_one({"id": entry_id, "type": entry_type})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"deleted": True}

from bson import ObjectId

@app.get("/drafts/{draft_id}", response_model=dict)
async def get_draft(draft_id: str):
    try:
        draft = await db.drafts.find_one({"_id": ObjectId(draft_id)})
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        return clean_mongo_doc(draft)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid draft ID format")

@app.post("/drafts/", response_model=dict)
async def create_draft(draft: dict):
    result = await db.drafts.insert_one(draft)
    draft["_id"] = str(result.inserted_id)
    return clean_mongo_doc(draft)

@app.put("/drafts/{draft_id}", response_model=dict)
async def update_draft(draft_id: str, data: dict = Body(...)):
    updated = await db.drafts.find_one_and_update(
        {"_id": ObjectId(draft_id)},
        {"$set": data},
        return_document=True,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Draft not found")
    return clean_mongo_doc(updated)
