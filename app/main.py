from fastapi import Depends, FastAPI
from sqlmodel import Session
from sqlalchemy import text

from app.database import get_session
from app.routes import router

app = FastAPI(title="CoreAssist AI")

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "CoreAssist AI is running"}


@app.get("/test-db")
def test_db(session: Session = Depends(get_session)):
    result = session.execute(text("SELECT 1")).scalar()
    return {"database_connection": result}