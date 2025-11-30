from pathlib import Path

def ocr_image(file_path: Path) -> str:
    """Mocks an OCR function, returning placeholder text for image processing."""
    print(f"MOCK OCR: Reading image file {file_path}")
    
    return "Vendor: Quantum Systems, Date: 2024-11-15, Invoice No: QS-9001, Item: Consultation Fee, Qty: 1, Price: 500.00, Tax: 50.00, Total: 550.00"