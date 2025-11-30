from typing import Dict, Any
from openai import OpenAI

class ValidationAgent:
    """Performs lightweight checks and data normalization."""
    def __init__(self, api_key: str):
        # Initialize OpenAI, though not strictly used in the validate method, keeping it for compatibility
        self.client = OpenAI(api_key=api_key) 

    def validate(self, extracted: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run lightweight checks and normalization:
         - Numbers parsed and cast (total, line item quantities, and prices).
        """
        data = extracted.copy()
        
        try:
            # Simple conversion to float for total
            total_val = data.get("total", 0)
            if isinstance(total_val, str):
                 # Attempt to clean up common currency symbols and commas
                total_val = total_val.replace('$', '').replace(',', '').strip()
            # Ensure proper casting and default to 0.0 if cleanup fails
            data["total"] = float(total_val or 0.0)
        except Exception:
            data["total"] = None
            
        # Ensure line_items is always a list
        if "line_items" not in data or not isinstance(data["line_items"], list):
            data["line_items"] = []
        else:
            # Iterate through line items and ensure qty/price are numeric
            cleaned_line_items = []
            for item in data["line_items"]:
                try:
                    # Clean and cast Quantity
                    qty_val = item.get("qty", 0)
                    if isinstance(qty_val, str):
                        qty_val = qty_val.replace(',', '').strip()
                    item["qty"] = float(qty_val or 0.0)
                    
                    # Clean and cast Price
                    price_val = item.get("price", 0)
                    if isinstance(price_val, str):
                        price_val = price_val.replace('$', '').replace(',', '').strip()
                    item["price"] = float(price_val or 0.0)
                    
                    cleaned_line_items.append(item)
                except Exception:
                    # Skip or log malformed items, preserving data integrity
                    pass
            data["line_items"] = cleaned_line_items
            
        return data