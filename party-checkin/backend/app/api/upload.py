import os
import shutil
from pathlib import Path

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi import HTTPException

from app.database import SessionLocal
from app.services.import_service import ImportService

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_FILE = Path("responses.xlsx")


@router.post("/excel")
async def upload_excel(file: UploadFile = File(...)):

    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an Excel (.xlsx) file."
        )

    with open(UPLOAD_FILE, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db = SessionLocal()

    try:

        service = ImportService(db)

        result = service.import_excel(str(UPLOAD_FILE))

        return {
            "success": True,
            "message": "Excel imported successfully.",
            "result": result
        }

    finally:
        db.close()