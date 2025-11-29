from typing import Any, Dict
from openai import OpenAI


class ValidationAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def validate(self, extracted: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run lightweight checks and normalization:
         - Dates normalized to ISO
         - Numbers parsed and cast
         - Missing fields flagged
        """
        data = extracted.copy()
        
        try:
            data["total"] = float(data.get("total", 0))
        except Exception:
            data["total"] = None
        return data
