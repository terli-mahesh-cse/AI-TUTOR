from datetime import date, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User, QuizAttempt, Badge, UserBadge
from app.routers.auth import get_current_user
from app.services.progress_tracker import (
    update_user_activity_and_streak,
    compute_weak_areas,
    get_daily_quota
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
templates = Jinja2Templates(directory="app/templates")

@router.get("", response_class=HTMLResponse)
def user_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    update_user_activity_and_streak(db, user)
    msg_count, quiz_count = get_daily_quota(db, user)

    # XP & Level Calculation
    total_xp = user.total_xp
    user_level = 1 + (total_xp // 100)
    current_level_xp = total_xp % 100

    # Quizzes stats
    quiz_attempts = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == user.id)
        .order_by(QuizAttempt.created_at.asc())
        .all()
    )

    chart_dates = [q.created_at.strftime("%b %d") for q in quiz_attempts[-10:]]
    chart_scores = [q.percentage for q in quiz_attempts[-10:]]

    # Weak areas
    weak_areas = compute_weak_areas(db, user.id)

    # Badges
    unlocked_ub = db.query(UserBadge).filter(UserBadge.user_id == user.id).all()
    unlocked_badge_ids = {ub.badge_id for ub in unlocked_ub}
    all_badges = db.query(Badge).all()

    unlocked_badges = [b for b in all_badges if b.id in unlocked_badge_ids]
    locked_badges = [b for b in all_badges if b.id not in unlocked_badge_ids]

    # 28-day Streak heatmap calculation
    today = date.today()
    heatmap_days = []
    for i in range(27, -1, -1):
        day_date = today - timedelta(days=i)
        is_active = (user.last_active_date == day_date) or (
            user.last_active_date and user.last_active_date >= day_date and i < user.streak_count
        )
        heatmap_days.append({
            "date": day_date.strftime("%b %d"),
            "active": is_active
        })

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
            "user_level": user_level,
            "current_level_xp": current_level_xp,
            "total_quizzes": len(quiz_attempts),
            "chart_dates": chart_dates,
            "chart_scores": chart_scores,
            "weak_areas": weak_areas,
            "unlocked_badges": unlocked_badges,
            "locked_badges": locked_badges,
            "heatmap_days": heatmap_days,
            "msg_count": msg_count,
            "quiz_count": quiz_count
        }
    )
