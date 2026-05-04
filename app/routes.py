from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Contact, Department, Document, Service

router = APIRouter(prefix="/api", tags=["resources"])


@router.get("/contacts")
def get_contacts(session: Session = Depends(get_session)):
    return session.exec(select(Contact)).all()


@router.get("/departments")
def get_departments(session: Session = Depends(get_session)):
    return session.exec(select(Department)).all()


@router.get("/documents")
def get_documents(session: Session = Depends(get_session)):
    return session.exec(select(Document)).all()


@router.get("/services")
def get_services(session: Session = Depends(get_session)):
    return session.exec(select(Service)).all()