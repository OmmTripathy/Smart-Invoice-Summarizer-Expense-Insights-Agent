from typing import Dict, Any
from openai import OpenAI

class ValidationAgent:
    """Performs lightweight checks and data normalization."""
    def __init__(self, api_key: str):
        
        self.client = OpenAI(api_key=api_key) 

    def validate(self, extracted: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run lightweight checks and normalization:
         - Numbers parsed and cast (total, line item quantities, and prices).
        """
        data = extracted.copy()
        
        try:
            
            total_val = data.get("total", 0)
            if isinstance(total_val, str):
                
                total_val = total_val.replace('$', '').replace(',', '').strip()
           
            data["total"] = float(total_val or 0.0)
        except Exception:
            data["total"] = None
            
        
        if "line_items" not in data or not isinstance(data["line_items"], list):
            data["line_items"] = []
        else:
          
            cleaned_line_items = []
            for item in data["line_items"]:
                try:
                    
                    qty_val = item.get("qty", 0)
                    if isinstance(qty_val, str):
                        qty_val = qty_val.replace(',', '').strip()
                    item["qty"] = float(qty_val or 0.0)
                    
                    
                    price_val = item.get("price", 0)
                    if isinstance(price_val, str):
                        price_val = price_val.replace('$', '').replace(',', '').strip()
                    item["price"] = float(price_val or 0.0)
                    
                    cleaned_line_items.append(item)
                except Exception:
                   
                    pass
            data["line_items"] = cleaned_line_items
            
        return data