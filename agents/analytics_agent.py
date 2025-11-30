from typing import Dict, Any
from openai import OpenAI

class AnalyticsAgent:
    """Generates summaries and provides conversational responses using OpenAI."""
    def __init__(self, api_key: str):
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=api_key)

    def summarize(self, cleaned: Dict[str, Any]) -> str:
        """Generates a summary, categories, and suggestions from the cleaned data."""
        prompt = (
            f"Given this invoice data: {cleaned}\n"
            f"Provide a short summary (2-3 sentences) and list top 3 expense categories and suggestions. Format the output clearly using bullet points for the categories/suggestions."
        )
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        
        # Return the raw text content for the insights display
        return resp.choices[0].message.content

    def chat_reply(self, prompt: str) -> str:
        """
        Answers general knowledge or invoice-specific queries using LLM.
        The system prompt guides the agent to answer all queries using its knowledge base.
        """
        system_prompt = (
            "You are a highly knowledgeable and friendly Expense Insights Agent. "
            "Your domain knowledge covers invoice data analysis, current affairs, and general knowledge. "
            "If the user asks a question about the 'CURRENT INVOICE DATA' provided in the context, please use that information to answer. "
            "For all other queries (current affairs, general knowledge, etc.), use your extensive knowledge base to provide a concise and helpful answer."
        )
        
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt} 
            ],
            max_tokens=300
        )
        
        return resp.choices[0].message.content