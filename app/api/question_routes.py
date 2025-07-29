from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.question_service import create_question, get_question
from app.tasks.background import simulate_answer_generation
from app.schemas.question import QuestionCreate, QuestionOut

router = APIRouter()


@router.post("/documents/{doc_id}/question", response_model=QuestionOut)
async def submit_question(
    doc_id: int,
    question_data: QuestionCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    question = await create_question(doc_id, question_data, db)
    background_tasks.add_task(simulate_answer_generation, question.id, question_data.question, db)
    return question


@router.get("/{question_id}", response_model=QuestionOut)
async def fetch_question(question_id: int, db: AsyncSession = Depends(get_db)):
    q = await get_question(question_id, db)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q
