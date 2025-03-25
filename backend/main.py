from fastapi import FastAPI, HTTPException, Body
from typing import Union
from fastapi.responses import FileResponse
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from models import ResumeData, TemplateOnly
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

# @app.on_event("startup")
# async def startup_db():
#     client = AsyncIOMotorClient(MONGO_URL)
#     await init_beanie(database=client.resume_db, document_models=[Resume])

@app.post("/generate-resume")
def generate_resume(
    payload: Union[ResumeData, TemplateOnly] = Body(...)):
    data = payload.dict()
    pdf_path = generate_pdf(data)
    return FileResponse(path=pdf_path, media_type="application/pdf", filename="resume.pdf")