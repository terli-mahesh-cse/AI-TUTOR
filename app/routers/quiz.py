from typing import Optional, List
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User, Subject, Lesson, QuizAttempt
from app.routers.auth import get_current_user
from app.services.quiz_generator import generate_quiz_questions
from app.services.progress_tracker import (
    update_user_activity_and_streak,
    get_daily_quota,
    increment_daily_quiz,
    check_and_award_badges
)

router = APIRouter(prefix="/quiz", tags=["quiz"])
templates = Jinja2Templates(directory="app/templates")

@router.get("", response_class=HTMLResponse)
def quiz_page(
    request: Request,
    topic: Optional[str] = None,
    subject_id: Optional[int] = None,
    lesson_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    update_user_activity_and_streak(db, user)
    _, quiz_count = get_daily_quota(db, user)

    subject = db.query(Subject).filter(Subject.id == subject_id).first() if subject_id else None
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first() if lesson_id else None
    
    topic_title = topic or (lesson.title if lesson else "General Knowledge")

    return templates.TemplateResponse(
        request=request,
        name="quiz.html",
        context={
            "user": user,
            "topic_title": topic_title,
            "subject": subject,
            "lesson": lesson,
            "quiz_count": quiz_count,
            "max_free_quizzes": 2
        }
    )

@router.post("/generate")
async def generate_quiz_endpoint(
    topic_title: str = Form(...),
    subject_name: str = Form("General"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Free tier quota check
    if not user.is_pro:
        _, quiz_count = get_daily_quota(db, user)
        if quiz_count >= 2:
            return JSONResponse(
                status_code=403,
                content={"detail": "Daily quiz limit reached. Upgrade to Pro for unlimited quizzes!"}
            )

    questions = await generate_quiz_questions(topic_title=topic_title, subject_name=subject_name)
    return JSONResponse(content={"questions": questions, "topic_title": topic_title})

@router.post("/submit")
def submit_quiz(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    update_user_activity_and_streak(db, user)
    increment_daily_quiz(db, user)

    topic_title = data.get("topic_title", "General Quiz")
    subject_id = data.get("subject_id")
    lesson_id = data.get("lesson_id")
    user_answers = data.get("answers", [])  # list of selected option indices
    questions = data.get("questions", [])

    correct_count = 0
    total = len(questions)

    for i, q in enumerate(questions):
        correct_idx = q.get("correct_index", 0)
        selected_idx = user_answers[i] if i < len(user_answers) else -1
        if selected_idx == correct_idx:
            correct_count += 1

    percentage = round((correct_count / total * 100.0), 1) if total > 0 else 0.0
    passed = percentage >= 70.0

    # XP logic: +20 XP for attempt, +5 XP per correct answer
    xp_earned = 20 + (correct_count * 5)
    user.total_xp += xp_earned
    db.commit()

    # Save attempt
    attempt = QuizAttempt(
        user_id=user.id,
        subject_id=subject_id,
        lesson_id=lesson_id,
        topic_title=topic_title,
        score=correct_count,
        total_questions=total,
        percentage=percentage,
        xp_earned=xp_earned
    )
    db.add(attempt)
    db.commit()
    db.refresh(user)

    unlocked_badges = check_and_award_badges(db, user)

    return JSONResponse(content={
        "score": correct_count,
        "total": total,
        "percentage": percentage,
        "xp_earned": xp_earned,
        "passed": passed,
        "unlocked_badges": unlocked_badges,
        "new_total_xp": user.total_xp
    })
