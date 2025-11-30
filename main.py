from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import os
import time
import json

# --- CRITICAL: IMPORT EXISTING AGENTS AND MANAGER ---
# We assume these modules are already defined and available in the environment.
from agents.extraction_agent import ExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.analytics_agent import AnalyticsAgent

from storage.session_manager import SessionManager


from dotenv import load_dotenv
import os

load_dotenv()   # Load .env

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_KEY:
    raise ValueError("OPENAI_API_KEY is missing in your .env file!")


# Initialize Agents globally using the imported classes
# This is done *without* declaring new agent classes, as requested.
session_db = SessionManager()
extractor = ExtractionAgent(api_key=OPENAI_KEY)
validator = ValidationAgent(api_key=OPENAI_KEY)
analytics = AnalyticsAgent(api_key=OPENAI_KEY)

app = FastAPI(title="Smart Invoice Summarizer & Expense Insights Agent")

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

# Path for the HTML file 
HTML_FILE_PATH = Path("index.html")

# --- DATA MODELS ---

class ChatRequest(BaseModel):
    prompt: str
    session_id: str = "default"

# --- API ENDPOINTS ---

@app.get("/")
async def serve_frontend():
    """Serves the main HTML frontend file."""
    if not HTML_FILE_PATH.exists():
        # Fallback error for missing frontend
        return HTMLResponse(
            content="<h1>Frontend Missing</h1><p>Please ensure 'index.html' is present in the root directory.</p>",
            status_code=404
        )
    return FileResponse(HTML_FILE_PATH)


@app.post("/process")
async def process_invoice(file: UploadFile = File(...), session_id: str = Form("default")):
    """Handles file upload, extraction, validation, and summarization using imported agents."""
    
    # 1. Save file to temporary storage for processing
    unique_filename = f"{int(time.time())}_{file.filename}"
    temp_file_path = UPLOAD_DIR / Path(unique_filename)
    
    try:
        # Read and write the file contents
        with open(temp_file_path, "wb") as f:
            while contents := await file.read(1024 * 1024):
                f.write(contents)
        
        # 2. Extraction (calls LLM/OCR/PDFplumber via the imported agent)
        raw_data = extractor.extract(temp_file_path)
        
        # 3. Validation/Cleaning (via the imported agent)
        cleaned = validator.validate(raw_data)
        
        # 4. Analytics/Insights (via the imported agent)
        insights = analytics.summarize(cleaned) 
        
        # 5. Update Session DB with latest data (via the imported manager)
        session_data = session_db.load(session_id) or {}
        # Store the current extracted data for chat context
        session_data["extractions"] = cleaned 
        session_db.save(session_id, session_data)
        
        return JSONResponse({"data": cleaned, "insights": insights})

    except Exception as e:
        print(f"Error during file processing: {e}")
        # Use an external tool to show internal process. [Image of ETL pipeline]
        raise HTTPException(status_code=500, detail=f"Internal Server Error during processing stage (Extraction -> Validation -> Summarization): {e}")
    finally:
        # Important: Delete the temporary file after successful processing
        if temp_file_path.exists():
            os.remove(temp_file_path)


@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles chat prompts, passing session context to the LLM agent."""
    prompt = request.prompt
    session_id = request.session_id

    # Load context from session
    session_data = session_db.load(session_id) or {}
    
    # 1. Prepare context for the LLM
    context = ""
    extracted_data = session_data.get("extractions")
    
    if extracted_data:
        # Include a clear section header for the LLM to easily identify invoice data
        context += f"CURRENT INVOICE DATA:\n{json.dumps(extracted_data, indent=2)}\n\n"
    
    full_prompt = context + f"USER QUERY: {prompt}"

    # 2. Use AnalyticsAgent to generate reply (via the imported agent)
    # The AnalyticsAgent is configured to answer both general knowledge and invoice queries.
    reply = analytics.chat_reply(full_prompt) 

    # 3. Update chat history in the session database (via the imported manager)
    chat_history = session_data.get("history", [])
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "agent", "content": reply})
    session_data["history"] = chat_history
    
    session_db.save(session_id, session_data)

    return {"reply": reply}