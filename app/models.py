from typing import Optional

from sqlmodel import Field, SQLModel

class Contact(SQLModel, table=True):
    __tablename__ = "contacts"

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str
    phone: Optional[str] = None
    department: Optional[str] = None
    job_title: Optional[str] = None
    department_id: Optional[int] = None


class Department(SQLModel, table=True):
    __tablename__ = "departments"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None


class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str
    file_name: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[int] = None



class Service(SQLModel, table=True):
    __tablename__ = "services"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    description: Optional[str] = None
    procedure: Optional[str] = None
    department_id: Optional[int] = None
    contact_id: Optional[int] = None
    document_id: Optional[int] = None