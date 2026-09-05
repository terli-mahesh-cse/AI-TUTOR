import json
from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Query, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User, Message, Subject, Lesson
from app.routers.auth import get_current_user
from app.services.claude_client import claude_client
from app.services.tutor_prompts import get_tutor_system_prompt
from app.services.progress_tracker import update_user_activity_and_streak, get_daily_quota, increment_daily_message

router = APIRouter(prefix="/chat", tags=["chat"])
templates = Jinja2Templates(directory="app/templates")

@router.get("", response_class=HTMLResponse)
def chat_page(
    request: Request,
    subject_id: Optional[int] = None,
    lesson_id: Optional[int] = None,
    topic: Optional[str] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    update_user_activity_and_streak(db, user)
    msg_count, _ = get_daily_quota(db, user)
    
    # Query past messages
    query = db.query(Message).filter(Message.user_id == user.id)
    if subject_id:
        query = query.filter(Message.subject_id == subject_id)
    messages = query.order_by(Message.created_at.asc()).all()

    active_subject = db.query(Subject).filter(Subject.id == subject_id).first() if subject_id else None
    active_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first() if lesson_id else None

    # Pre-seed initial message if specified via query param and chat is empty
    initial_prompt = ""
    if topic:
        initial_prompt = f"Hi! I'd like to learn about {topic}."
    elif active_lesson:
        initial_prompt = active_lesson.initial_prompt

    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "user": user,
            "messages": messages,
            "active_subject": active_subject,
            "active_lesson": active_lesson,
            "initial_prompt": initial_prompt,
            "msg_count": msg_count,
            "max_free_msgs": 10
        }
    )

@router.post("/send")
def send_message(
    request: Request,
    content: str = Form(...),
    subject_id: Optional[int] = Form(None),
    lesson_id: Optional[int] = Form(None),
    is_socratic: bool = Form(True),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    update_user_activity_and_streak(db, user)
    
    # Check free quota
    if not user.is_pro:
        msg_count, _ = get_daily_quota(db, user)
        if msg_count >= 10:
            return templates.TemplateResponse(
                request=request,
                name="chat_quota_warning.html",
                context={"user": user}
            )

    increment_daily_message(db, user)

    # Save student message
    student_msg = Message(
        user_id=user.id,
        subject_id=subject_id,
        lesson_id=lesson_id,
        sender="student",
        content=content.strip(),
        is_socratic=is_socratic
    )
    db.add(student_msg)
    db.commit()
    db.refresh(student_msg)

    return templates.TemplateResponse(
        request=request,
        name="partials/chat_message_bubble.html",
        context={
            "message": student_msg,
            "subject_id": subject_id,
            "lesson_id": lesson_id,
            "is_socratic": is_socratic,
            "user": user
        }
    )

@router.get("/stream")
async def stream_chat(
    request: Request,
    content: str = Query(...),
    subject_id: Optional[int] = Query(None),
    lesson_id: Optional[int] = Query(None),
    is_socratic: bool = Query(True),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Retrieve subject name
    subject_name = "General"
    if subject_id:
        sub = db.query(Subject).filter(Subject.id == subject_id).first()
        if sub:
            subject_name = sub.name

    system_prompt = get_tutor_system_prompt(subject_name=subject_name, is_socratic=is_socratic)

    # Fetch last 6 messages for context
    past_msgs = (
        db.query(Message)
        .filter(Message.user_id == user.id)
        .order_by(Message.created_at.desc())
        .limit(6)
        .all()
    )
    past_msgs.reverse()

    formatted_messages = []
    for m in past_msgs:
        role = "user" if m.sender == "student" else "assistant"
        formatted_messages.append({"role": role, "content": m.content})
    
    if not formatted_messages or formatted_messages[-1]["content"] != content:
        formatted_messages.append({"role": "user", "content": content})

    async def event_generator():
        full_response_acc = []
        async for chunk in claude_client.stream_chat_response(system_prompt, formatted_messages):
            full_response_acc.append(chunk)
            # Send SSE event format
            event_data = json.dumps({"token": chunk})
            yield f"data: {event_data}\n\n"
        
        # Save complete tutor message to DB
        tutor_reply = "".join(full_response_acc)
        tutor_msg = Message(
            user_id=user.id,
            subject_id=subject_id,
            lesson_id=lesson_id,
            sender="tutor",
            content=tutor_reply,
            is_socratic=is_socratic
        )
        db.add(tutor_msg)
        db.commit()
        
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
