from typing import Dict, Any
from openai import OpenAI
import json
from pathlib import Path


from tools.image_ocr import ocr_image
from tools.pdf_extractor import extract_pdf_text


class ExtractionAgent:
    """Handles document text extraction (PDFplumber/OCR) and LLM-based structured data parsing."""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def extract(self, file_path: Path) -> Dict[str, Any]:
        """
        Extracts raw text and uses LLM to parse structured invoice data.
        """
        text = ""
        
       
        file_name = str(file_path).lower()
        if file_name.endswith(".pdf"):
            text = extract_pdf_text(file_path)
        elif file_name.endswith(('.png', '.jpg', '.jpeg')):
            text = ocr_image(file_path)
        else:
            return {"error": "Unsupported file type."}

        
        prompt = (
            f"Extract invoice fields from the following text. Return a raw JSON object with the following fields: "
            f"vendor, date, invoice_number, line_items (list of objects with description, qty, price), subtotal, tax, total. "
            f"If a field is missing, use null or 0.00 where appropriate. "
            f"IMPORTANT: ONLY return the raw JSON object, do not include markdown backticks or any explanation.\n\nTEXT:\n{text[:6000]}"
        )
        
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role":"user","content":prompt}],
            max_tokens=800,
            response_format={"type": "json_object"}
        )
        
        llm_text = resp.choices[0].message.content
        
        try:
            return json.loads(llm_text)
        except Exception as e:
            print(f"Error parsing LLM JSON output: {e}")
            return {"raw_text": text, "llm_output": llm_text, "error": str(e)}