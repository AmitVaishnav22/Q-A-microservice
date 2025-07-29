from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.document import DocumentCreate, DocumentOut
from app.services.document_service import create_document, get_document

router = APIRouter()


@router.post("/", response_model=DocumentOut)
async def upload_document(document: DocumentCreate, db: AsyncSession = Depends(get_db)):
    return await create_document(document, db)


@router.get("/{doc_id}", response_model=DocumentOut)
async def fetch_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    doc = await get_document(doc_id, db)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
