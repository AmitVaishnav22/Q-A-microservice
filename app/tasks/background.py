import google.generativeai as genai
from app.db.models import Question, QuestionStatus
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def simulate_answer_generation(question_id: int, question_text: str, db: AsyncSession):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(question_text)
        answer = response.text.strip()
        #print(f"[Gemini] Generated answer: {answer}")
        stmt = (
            update(Question)
            .where(Question.id == question_id)
            .values(answer=answer, status=QuestionStatus.answered)
        )
        await db.execute(stmt)
        await db.commit()

    except Exception as e:
        fallback_answer = (
            "AI model couldn't generate a response now due to quota limits. "
            "Please try again later."
        )
        stmt = (
            update(Question)
            .where(Question.id == question_id)
            .values(answer=fallback_answer, status=QuestionStatus.answered)
        )
        await db.execute(stmt)
        await db.commit()
        #print(f"[Gemini ERROR] Failed to generate answer: {e}")
