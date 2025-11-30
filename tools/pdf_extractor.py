import pdfplumber
from pathlib import Path

def extract_pdf_text(file_path: Path) -> str:
    """Extracts raw text content from a PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error during PDF extraction: {e}")
        return f"Error extracting PDF text: {e}"
    
    return text