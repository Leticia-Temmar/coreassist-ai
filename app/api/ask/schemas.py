from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    context: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    parameters: Dict[str, Any] = Field(default_factory=dict)


class AskResponse(BaseModel):
    status: str
    context: str
    question: str
    result: Optional[Any] = None
    message: Optional[str] = None

class AskRagRequest(BaseModel):
    question: str