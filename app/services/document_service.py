from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Document
from app.schemas.document import DocumentCreate


async def create_document(document: DocumentCreate, db: AsyncSession) -> Document:
    try:
        new_doc = Document(title=document.title, content=document.content)
        db.add(new_doc)
        await db.commit()
        await db.refresh(new_doc)
        return new_doc
    except Exception as e:
        await db.rollback()
        raise e


async def get_document(doc_id: int, db: AsyncSession) -> Document | None:
    try:
        result = await db.execute(select(Document).where(Document.id == doc_id))
        return result.scalar_one_or_none()
    except Exception as e:
        await db.rollback()
        raise e