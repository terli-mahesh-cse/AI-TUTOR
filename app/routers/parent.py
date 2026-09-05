from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User, QuizAttempt, UserBadge, Badge
from app.services.progress_tracker import compute_weak_areas

router = APIRouter(prefix="/parent", tags=["parent"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/{share_token}", response_class=HTMLResponse)
def parent_dashboard(share_token: str, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.parent_share_token == share_token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Student progress report not found or link expired.")

    user_level = 1 + (user.total_xp // 100)
    quiz_attempts = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == user.id)
        .order_by(QuizAttempt.created_at.desc())
        .all()
    )

    chart_dates = [q.created_at.strftime("%b %d") for q in reversed(quiz_attempts[:10])]
    chart_scores = [q.percentage for q in reversed(quiz_attempts[:10])]

    weak_areas = compute_weak_areas(db, user.id)

    unlocked_ub = db.query(UserBadge).filter(UserBadge.user_id == user.id).all()
    unlocked_badge_ids = {ub.badge_id for ub in unlocked_ub}
    all_badges = db.query(Badge).all()
    unlocked_badges = [b for b in all_badges if b.id in unlocked_badge_ids]

    return templates.TemplateResponse(
        request=request,
        name="parent_dashboard.html",
        context={
            "student": user,
            "user_level": user_level,
            "quiz_attempts": quiz_attempts,
            "chart_dates": chart_dates,
            "chart_scores": chart_scores,
            "weak_areas": weak_areas,
            "unlocked_badges": unlocked_badges
        }
    )
