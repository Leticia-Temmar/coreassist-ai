import os
from google import genai
from app.rag.search_contacts import search_similar_contacts
from google.genai import errors

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def answer_contacts_question(user_question: str):
    results = search_similar_contacts(user_question, limit=5)

    context = "\n\n".join(
        item["content"] for item in results
    )

    prompt = f"""
You are an internal company assistant.

Use only the context below to answer the user's question.
If the answer is not in the context, say that you do not have enough information.

Context:
{context}

User question:
{user_question}

Answer clearly and concisely.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text

    except errors.ClientError:
        return "AI unavailable (quota exceeded or API issue), but retrieval system is working."

if __name__ == "__main__":
    answer = answer_contacts_question(
        "Who works in Software Engineering department?"
    )

    print(answer)