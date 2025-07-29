from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Question, QuestionStatus
from app.schemas.question import QuestionCreate


async def create_question(document_id: int, question_data: QuestionCreate, db: AsyncSession) -> Question:
    try:
        q = Question(
            document_id=document_id,
            question=question_data.question,
            status=QuestionStatus.pending
        )
        db.add(q)
        await db.commit()
        await db.refresh(q)
        return q
    except Exception as e:
        await db.rollback()
        raise e


async def get_question(question_id: int, db: AsyncSession) -> Question | None:
    try:
        result = await db.execute(select(Question).where(Question.id == question_id))
        return result.scalar_one_or_none()
    except Exception as e:
        await db.rollback()
        raise e
