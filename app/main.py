from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from agents.extraction_agent import ExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.analytics_agent import AnalyticsAgent
from pathlib import Path

from storage.session_manager import SessionManager
session_db = SessionManager()

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="Smart Invoice Summarizer & Expense Insights Agent")

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/process")
async def process_invoice(file: UploadFile = File(...)):
   
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    
    extractor = ExtractionAgent(api_key=OPENAI_KEY)
    raw_data = extractor.extract(file_path)

    validator = ValidationAgent(api_key=OPENAI_KEY)
    cleaned = validator.validate(raw_data)

    analytics = AnalyticsAgent(api_key=OPENAI_KEY)
    insights = analytics.summarize(cleaned)

    return JSONResponse({"data": cleaned, "insights": insights})

@app.post("/chat")
async def chat(prompt: str = Form(...), session_id: str = Form("default")):
    old_data = session_db.load(session_id) or {}

    combined = {
        "history": old_data.get("history", []),
        "extractions": old_data.get("extractions", []),
    }

    combined["history"].append({"user": prompt})

    analytics = AnalyticsAgent(api_key=OPENAI_KEY)
    reply = analytics.chat_reply(prompt)

    combined["history"].append({"agent": reply})

    session_db.save(session_id, combined)

    return {"reply": reply}

