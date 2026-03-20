from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ocr import process_document

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF/image) and extract text with OCR.
    """
    if not file.filename.endswith(('.pdf', '.png', '.jpg', '.jpeg')):
        raise HTTPException(400, "Unsupported format")
    
    content = await file.read()
    text = process_document(content)
    return {"filename": file.filename, "text": text}