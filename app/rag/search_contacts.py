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

def search_similar_contacts(user_question: str, limit: int = 3):
    question_embedding = generate_embedding(user_question)

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT contact_id, content, embedding
            FROM contact_embeddings
        """))

        similarities = []

        for row in result:
            score = cosine_similarity(question_embedding, row.embedding)

            similarities.append({
                "contact_id": row.contact_id,
                "content": row.content,
                "score": score
            })

        similarities.sort(key=lambda item: item["score"], reverse=True)

        return similarities[:limit]
    
if __name__ == "__main__":
    results = search_similar_contacts("Who works in Software Engineering department?")

    for item in results:
        print(item["score"])
        print(item["content"])