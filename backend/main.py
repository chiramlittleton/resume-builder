from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import Resume
from generate import generate_pdf
import os

app = FastAPI()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

@app.on_event("startup")
async def startup_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client.resume_db, document_models=[Resume])

@app.post("/generate-resume")
async def generate_resume(resume: Resume):
    await resume.insert()
    pdf_path = generate_pdf(resume.dict())
    return FileResponse(pdf_path, media_type="application/pdf", filename="resume.pdf")
