from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.params import Body

from backend.api.routes.util import clean_mongo_doc
from backend.db.mongo import db

router = APIRouter()

@router.get("/drafts", response_model=List[dict])
async def get_drafts():
    drafts = await db.drafts.find().to_list(None)
    return [clean_mongo_doc(d) for d in drafts]

@router.get("/drafts/{draft_id}", response_model=dict)
async def get_draft(draft_id: str):
    try:
        draft = await db.drafts.find_one({"_id": ObjectId(draft_id)})
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        return clean_mongo_doc(draft)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid draft ID format")

@router.post("/drafts/", response_model=dict)
async def create_draft(draft: dict):
    result = await db.drafts.insert_one(draft)
    draft["_id"] = str(result.inserted_id)
    return clean_mongo_doc(draft)

@router.put("/drafts/{draft_id}", response_model=dict)
async def update_draft(draft_id: str, data: dict = Body(...)):
    updated = await db.drafts.find_one_and_update(
        {"_id": ObjectId(draft_id)},
        {"$set": data},
        return_document=True,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Draft not found")
    return clean_mongo_doc(updated)
