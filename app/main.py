from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlmodel import Session

from app.api.ask.routes import router as ask_router
from app.database import get_session
from app.routes import router as resources_router
from app.api.ask.routes import router as ask_rag_router
app = FastAPI(title="CoreAssist AI")

app.include_router(resources_router)
app.include_router(ask_router)
app.include_router(ask_rag_router)


@app.get("/")
def read_root():
    return {"message": "CoreAssist AI is running"}


@app.get("/test-db")
def test_db(session: Session = Depends(get_session)):
    result = session.execute(text("SELECT 1")).scalar()
    return {"database_connection": result}