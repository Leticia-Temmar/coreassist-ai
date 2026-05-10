import os
import time
import pdfplumber
from google import genai
from sqlalchemy import text

from app.database import engine

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

PDF_PATH = "app/documents/RH_Admin_Final_v2.pdf"


def extract_text_from_pdf(pdf_path: str) -> str:
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    return full_text


def chunk_text(text: str, chunk_size: int = 800) -> list[str]:
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def generate_embedding(text_input: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text_input
    )
    return response.embeddings[0].values


def ingest_pdf():
    document_name = os.path.basename(PDF_PATH)

    full_text = extract_text_from_pdf(PDF_PATH)
    chunks = chunk_text(full_text)

    with engine.connect() as connection:
        for chunk in chunks:
            embedding = generate_embedding(chunk)

            connection.execute(
                text("""
                    INSERT INTO document_chunks 
                    (document_name, chunk_text, embedding)
                    VALUES (:document_name, :chunk_text, :embedding)
                """),
                {
                    "document_name": document_name,
                    "chunk_text": chunk,
                    "embedding": embedding
                }
            )

            connection.commit()
            time.sleep(5)

    print(f"{len(chunks)} chunks inserted for {document_name}")


if __name__ == "__main__":
    ingest_pdf()