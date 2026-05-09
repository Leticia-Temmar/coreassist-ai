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
    You are CoreAssist AI, an intelligent internal company assistant.

    Your role is to answer in a natural, professional and friendly way.

    Rules:
    - Use ONLY the provided context for company-related questions
    - If the user greets you, respond politely with a greeting
    - For standard questions, do NOT greet again
    - Be concise, modern and professional
    - Format contact information clearly
    - If information is missing, politely say you could not find it


    Example greeting response:
    "Hello 👋 I'm CoreAssist AI. How can I help you today?"

    Context:
    {context}

    Question:
    {user_question}
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