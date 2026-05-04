from google import genai
import os
from app.database import engine
from sqlalchemy import text
import time

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def build_text(row):
    return f"""
Name: {row.full_name}
Department: {row.department} department
Job title: {row.job_title}
Email: {row.email}
"""

def generate_embedding(text_input):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text_input
    )
    return response.embeddings[0].values

def process_contacts():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, full_name, department, job_title, email
            FROM contacts
            WHERE id NOT IN (
                SELECT contact_id FROM contact_embeddings
            )
        """))

        for row in result:
            text_data = build_text(row)
            embedding = generate_embedding(text_data)

            conn.execute(text("""
                INSERT INTO contact_embeddings (contact_id, content, embedding)
                VALUES (:contact_id, :content, :embedding)
            """), {
                "contact_id": row.id,
                "content": text_data,
                "embedding": embedding
            })

            conn.commit()
            print(f"Processed contact {row.id}")
            time.sleep(5)

if __name__ == "__main__":
    process_contacts()