import os
from google import genai

from app.rag.pdf.search_pdf_chunks import search_pdf_chunks

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def answer_pdf_question(user_question: str) -> str:
    chunks = search_pdf_chunks(user_question, limit=3)

    context = "\n\n".join(
        chunk["chunk_text"] for chunk in chunks
    )

    prompt = f"""
    You are CoreAssist AI, an intelligent internal company assistant.

    Your role is to answer in a natural, professional and friendly way.

    Rules:
    - Use ONLY the provided context for company-related questions
    - If the user greets you, respond politely with a greeting
    - For standard questions, do NOT greet again
    - Be concise, modern and professional
    - Answer in English
    - If information is missing, politely say you could not find the information
    - Do not invent company policies or procedures
    - Summarize information clearly and naturally

    Example greeting response:
    "Hello 👋 I'm CoreAssist AI. How can I help you today?"

    Context:
    {context}

    Question:
    {user_question}
    """

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    answer = answer_pdf_question("Comment je pose mes jours ?")
    print(answer)