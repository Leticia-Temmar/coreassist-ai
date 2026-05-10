import os
import math

from google import genai
from sqlalchemy import text

from app.database import engine

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_embedding(text_input: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text_input
    )

    return response.embeddings[0].values


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0

    return dot_product / (norm_a * norm_b)


def search_pdf_chunks(user_question: str, limit: int = 3):
    question_embedding = generate_embedding(user_question)

    similarities = []

    with engine.connect() as connection:
        results = connection.execute(
            text("""
                SELECT document_name, chunk_text, embedding
                FROM document_chunks
            """)
        )

        for row in results:
            similarity_score = cosine_similarity(
                question_embedding,
                row.embedding
            )

            similarities.append({
                "document_name": row.document_name,
                "chunk_text": row.chunk_text,
                "score": similarity_score
            })

    similarities.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return similarities[:limit]


if __name__ == "__main__":
    results = search_pdf_chunks(
        "Comment je pose mes jours ?"
    )

    for result in results:
        print("\n")
        print("Score:", result["score"])
        print("Document:", result["document_name"])
        print("Chunk:", result["chunk_text"][:500])