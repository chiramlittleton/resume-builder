from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

@router.get("/templates")
async def get_templates():
    template_dir = Path("templates")
    templates = [
        f.name.replace(".tex.j2", "") for f in template_dir.glob("*.tex.j2")
    ]
    return templates