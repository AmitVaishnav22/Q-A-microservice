from fastapi import FastAPI
from app.api.document_routes import router as document_router
from app.api.question_routes import router as question_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Q&A Microservice",
    description="Handles document ingestion and question-answering.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(document_router, prefix="/documents", tags=["Documents"])
app.include_router(question_router, prefix="/questions", tags=["Questions"])

# Root
@app.get("/")
async def root():
    return {"message": "Q&A Microservice is running"}
