from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.ask.schemas import AskRequest, AskResponse, AskRagRequest
from app.database import get_session
from app.llm.parser import parse_user_question
from app.models import Service
from app.rag.answer_contacts import answer_contacts_question

router = APIRouter(prefix="/ask", tags=["ask"])


def get_service_description(session: Session, parameters: dict):
    service_name = parameters.get("name")

    if not service_name:
        raise HTTPException(status_code=400, detail="Missing parameter: name")

    statement = select(Service).where(Service.name == service_name)
    service = session.exec(statement).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return {
        "name": service.name,
        "description": service.description,
    }


ASK_MAPPING = {
    "service": {
        "get_service_description": get_service_description,
    }
}


@router.post("/", response_model=AskResponse)
async def ask(
    payload: AskRequest,
    session: Session = Depends(get_session),
) -> AskResponse:
    context = payload.context
    question = payload.question
    parameters = payload.parameters or {}

    if context not in ASK_MAPPING:
        raise HTTPException(status_code=400, detail="Unsupported context")

    if question not in ASK_MAPPING[context]:
        raise HTTPException(status_code=400, detail="Unsupported question")

    handler = ASK_MAPPING[context][question]
    result = handler(session, parameters)

    return AskResponse(
        status="success",
        context=context,
        question=question,
        result=result,
    )


@router.post("/llm")
async def ask_with_llm(
    payload: dict,
    session: Session = Depends(get_session),
):
    user_input = payload.get("user_input")

    if not user_input:
        raise HTTPException(status_code=400, detail="Missing user_input")

    parsed = parse_user_question(user_input)

    context = parsed.get("context")
    question = parsed.get("question")
    parameters = parsed.get("parameters", {})

    if context not in ASK_MAPPING:
        raise HTTPException(status_code=400, detail="Unsupported context")

    if question not in ASK_MAPPING[context]:
        raise HTTPException(status_code=400, detail="Unsupported question")

    handler = ASK_MAPPING[context][question]
    result = handler(session, parameters)

    return {
        "status": "success",
        "input": user_input,
        "parsed": parsed,
        "result": result,
    }

@router.post("/rag")
def ask_rag(request: AskRagRequest):
    answer = answer_contacts_question(request.question)

    return {
        "question": request.question,
        "answer": answer,
        "mode": "rag_with_llm"
    }