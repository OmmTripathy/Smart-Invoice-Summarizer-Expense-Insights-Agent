from typing import Dict, Any
from openai import OpenAI


class AnalyticsAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def summarize(self, cleaned: Dict[str, Any]) -> Dict[str, Any]:
        prompt = (
            f"Given this invoice data: {cleaned}\n"
            f"Provide a short summary (2-3 sentences) and list top 3 expense categories and suggestions."
        )
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )

        
        text = resp.choices[0].message.content

        return {"summary": text}

    def chat_reply(self, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        
        return resp.choices[0].message.content
