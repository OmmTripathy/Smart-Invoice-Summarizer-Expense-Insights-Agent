import os
from typing import Any, Dict
import pdfplumber
import tempfile
from openai import OpenAI


class ExtractionAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
     
        self.client = OpenAI(api_key=api_key)

    def extract(self, file_path) -> Dict[str, Any]:
        """
        Basic pipeline:
         - If PDF: run pdf text extraction (pdfplumber)
         - If image: call OCR tool
         - Then call LLM prompt to parse fields (vendor, date, line items, totals)
        """
        text = ""
        if str(file_path).lower().endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        else:
           
            from tools.image_ocr import ocr_image
            text = ocr_image(file_path)

        
        prompt = f"Extract invoice fields from the following text. Return JSON with vendor, date, invoice_number, line_items (description, qty, price), subtotal, tax, total.\n\nTEXT:\n{text[:6000]}"
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role":"user","content":prompt}],
            max_tokens=800
        )
        
        llm_text = resp.choices[0].message.content
        
        import json, re
        json_texts = re.findall(r"\{.*\}", llm_text, re.DOTALL)
        if json_texts:
            try:
                return json.loads(json_texts[0])
            except Exception:
                pass
     
        return {"raw_text": text, "llm_output": llm_text}
