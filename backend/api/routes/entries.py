from fastapi import APIRouter, HTTPException
from fastapi.params import Body

from backend.api.util import clean_for_rest
from backend.db.mongo import db
from typing import List

router = APIRouter()

@router.post("/entries/", response_model=dict)
async def create_entry(entry: dict):
    result = await db.entries.insert_one(entry)
    entry["_id"] = str(result.inserted_id)
    return entry

@router.get("/entries/{entry_type}", response_model=List[dict])
async def get_entries(entry_type: str):
    entries = await db.entries.find({"type": entry_type}).to_list(length=None)
    return [clean_for_rest(e) for e in entries]

@router.get("/entries/{entry_type}/{entry_id}", response_model=dict)
async def get_entry(entry_type: str, entry_id: str):
    entry = await db.entries.find_one({"id": entry_id, "type": entry_type})
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.put("/entries/{entry_type}/{entry_id}", response_model=dict)
async def update_entry(entry_type: str, entry_id: str, data: dict = Body(...)):
    result = await db.entries.find_one_and_update(
        {"id": entry_id, "type": entry_type}, {"$set": data}, return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Entry not found")
    return clean_for_rest(result)

@router.delete("/entries/{entry_type}/{entry_id}", response_model=dict)
async def delete_entry(entry_type: str, entry_id: str):
    result = await db.entries.delete_one({"id": entry_id, "type": entry_type})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"deleted": True}
