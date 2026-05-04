import json
import os
from fastapi import HTTPException
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """
You are an assistant that converts user questions into structured JSON.

Return ONLY valid JSON.

Allowed contexts:
- service

Allowed questions:
- get_service_description

Format:
{
  "context": "service",
  "question": "get_service_description",
  "parameters": {
    "name": "service_name"
  }
}
"""

def parse_user_question(user_input: str) -> dict:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\nUser: {user_input}"
        )

        content = response.text.strip()

        if content.startswith("```json"):
          content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
          content = content.replace("```", "").strip()
        return json.loads(content)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )