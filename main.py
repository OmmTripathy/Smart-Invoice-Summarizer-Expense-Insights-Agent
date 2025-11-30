from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import os
import time
import json


from agents.extraction_agent import ExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.analytics_agent import AnalyticsAgent

from storage.session_manager import SessionManager


from dotenv import load_dotenv
import os

load_dotenv()  

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_KEY:
    raise ValueError("OPENAI_API_KEY is missing in your .env file!")



session_db = SessionManager()
extractor = ExtractionAgent(api_key=OPENAI_KEY)
validator = ValidationAgent(api_key=OPENAI_KEY)
analytics = AnalyticsAgent(api_key=OPENAI_KEY)

app = FastAPI(title="Smart Invoice Summarizer & Expense Insights Agent")

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)


HTML_FILE_PATH = Path("index.html")


class ChatRequest(BaseModel):
    prompt: str
    session_id: str = "default"



@app.get("/")
async def serve_frontend():
    """Serves the main HTML frontend file."""
    if not HTML_FILE_PATH.exists():
        
        return HTMLResponse(
            content="<h1>Frontend Missing</h1><p>Please ensure 'index.html' is present in the root directory.</p>",
            status_code=404
        )
    return FileResponse(HTML_FILE_PATH)


@app.post("/process")
async def process_invoice(file: UploadFile = File(...), session_id: str = Form("default")):
    """Handles file upload, extraction, validation, and summarization using imported agents."""
    
    
    unique_filename = f"{int(time.time())}_{file.filename}"
    temp_file_path = UPLOAD_DIR / Path(unique_filename)
    
    try:
        
        with open(temp_file_path, "wb") as f:
            while contents := await file.read(1024 * 1024):
                f.write(contents)
        
        
        raw_data = extractor.extract(temp_file_path)
        
        
        cleaned = validator.validate(raw_data)
        
        
        insights = analytics.summarize(cleaned) 
        
       
        session_data = session_db.load(session_id) or {}
        
        session_data["extractions"] = cleaned 
        session_db.save(session_id, session_data)
        
        return JSONResponse({"data": cleaned, "insights": insights})

    except Exception as e:
        print(f"Error during file processing: {e}")
        
        raise HTTPException(status_code=500, detail=f"Internal Server Error during processing stage (Extraction -> Validation -> Summarization): {e}")
    finally:
        
        if temp_file_path.exists():
            os.remove(temp_file_path)


@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles chat prompts, passing session context to the LLM agent."""
    prompt = request.prompt
    session_id = request.session_id

    
    session_data = session_db.load(session_id) or {}
    
    
    context = ""
    extracted_data = session_data.get("extractions")
    
    if extracted_data:
        
        context += f"CURRENT INVOICE DATA:\n{json.dumps(extracted_data, indent=2)}\n\n"
    
    full_prompt = context + f"USER QUERY: {prompt}"

    
    reply = analytics.chat_reply(full_prompt) 

   
    chat_history = session_data.get("history", [])
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "agent", "content": reply})
    session_data["history"] = chat_history
    
    session_db.save(session_id, session_data)

    return {"reply": reply}