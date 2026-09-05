from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Subject, Lesson, QuizAttempt, Progress
from app.routers.auth import get_current_user_optional

router = APIRouter(prefix="/subjects", tags=["subjects"])
templates = Jinja2Templates(directory="app/templates")

@router.get("", response_class=HTMLResponse)
def subjects_library(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    subjects = db.query(Subject).all()

    # Calculate completion percentage for each subject
    subject_progress = {}
    if user:
        attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == user.id).all()
        passed_topics = {a.topic_title for a in attempts if a.percentage >= 70.0}
        
        for s in subjects:
            total_lessons = len(s.lessons)
            if total_lessons > 0:
                completed = sum(1 for l in s.lessons if l.title in passed_topics)
                pct = int((completed / total_lessons) * 100)
            else:
                pct = 0
            subject_progress[s.id] = pct
    else:
        for s in subjects:
            subject_progress[s.id] = 0

    return templates.TemplateResponse(
        request=request,
        name="subjects.html",
        context={
            "user": user,
            "subjects": subjects,
            "subject_progress": subject_progress
        }
    )

@router.get("/{slug}", response_class=HTMLResponse)
def subject_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    subject = db.query(Subject).filter(Subject.slug == slug).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    lessons = db.query(Lesson).filter(Lesson.subject_id == subject.id).order_by(Lesson.order.asc()).all()

    passed_topics = set()
    if user:
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == user.id, QuizAttempt.subject_id == subject.id
        ).all()
        passed_topics = {a.topic_title for a in attempts if a.percentage >= 70.0}

    return templates.TemplateResponse(
        request=request,
        name="subject_detail.html",
        context={
            "user": user,
            "subject": subject,
            "lessons": lessons,
            "passed_topics": passed_topics
        }
    )
