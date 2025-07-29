#  Q&A Backend (FastAPI) MICROSERVICE

A lightweight backend service that allows users to submit questions and receive AI-generated answers using Google’s Gemini API. Built with FastAPI, SQLAlchemy, and asynchronous background processing.

---

##  Features

- Ask natural language questions via REST API
- Generates answers using Gemini 1.5 Pro (Google AI)
- Background task processing for async answer generation
- PostgreSQL + SQLAlchemy ORM
- Handles quota limits and fallback logic
- View question status and generated answers via status endpoint

---

## 📦 Tech Stack

| Layer       | Tool                   |
|-------------|------------------------|
| Backend     | FastAPI (async)        |
| AI Service  | Google Gemini API      |
| Database    | PostgreSQL (via SQLAlchemy) |
| ORM         | SQLAlchemy |
| Background Tasks | FastAPI `BackgroundTasks` |
| Deployment  | Docker / Render / Railway-ready |

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/AmitVaishnav22/ Q-A-microservice.git
cd gemini-fastapi-qa
```

### 2. Install dependencies

> Requires Python 3.10+

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

### 4. Run the app

```bash
uvicorn app.main:app --reload
```

> App will run at `http://localhost:8000`

---

## 📬 API Endpoints

### `POST /questions/documents/{doc_id}/question`
Submit a question

```json
{
  "document_id": 1,
  "question": "What is FastAPI?"
}
```

- Triggers background generation of the answer.
- Returns `question_id` for tracking.

---

### `GET /{question_id}`
Check the status of a submitted question

**Response:**

```json
{
  "status": "answered",
  "answer": "FastAPI is a modern web framework for building APIs in Python..."
}
```

Possible statuses:
- `pending`
- `answered`
- `failed`

---

## Gemini Quota Handling

The system automatically detects Gemini API quota errors (e.g. 429s) and:
- Marks questions as `failed`
- Stores a fallback message for the answer
- Can retry a few times before failing

---

## Example Flow

```bash
# Ask a question
curl -X POST http://localhost:8000/ask   -H "Content-Type: application/json"   -d '{"document_id": 1, "question": "What is FastAPI?"}'

# → Response: { "question_id": 4 }

# Later, check status
curl http://localhost:8000/status/4
```

---

##  Folder Structure

```
app/
├── api                   # API routes
├── db                    # DB connection logic
├── schemas               # Pydantic schemas
├── services/             # dbLogics
├── tasks/                # background tasks
├── utils/                # for creating tables
|__ main.py               # FastAPI entrypoint

```

## Future Improvements

- Add frontend (React/Vite) to submit/view answers
- Add API rate limiting & user auth
- Add caching for duplicate questions
- Add metrics dashboard (e.g., total questions, success/failure rate)

---

## License

MIT © 2025 Amit Vaishnav