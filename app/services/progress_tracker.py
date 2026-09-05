from datetime import date, timedelta
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import User, QuizAttempt, Progress, Badge, UserBadge, DailyQuota

def update_user_activity_and_streak(db: Session, user: User) -> int:
    today = date.today()
    if user.last_active_date is None:
        user.streak_count = 1
        user.last_active_date = today
    elif user.last_active_date == today:
        pass  # Already active today
    elif user.last_active_date == today - timedelta(days=1):
        user.streak_count += 1
        user.last_active_date = today
    else:
        user.streak_count = 1
        user.last_active_date = today
    
    db.commit()
    db.refresh(user)
    return user.streak_count

def check_and_award_badges(db: Session, user: User) -> List[str]:
    unlocked_codes = []
    unlocked_badge_ids = {ub.badge_id for ub in user.badges}
    all_badges = db.query(Badge).all()

    # Criteria checks
    total_quizzes = db.query(QuizAttempt).filter(QuizAttempt.user_id == user.id).count()
    has_perfect = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == user.id, QuizAttempt.percentage == 100.0
    ).first() is not None

    for badge in all_badges:
        if badge.id in unlocked_badge_ids:
            continue
        
        should_unlock = False
        if badge.code == "first_quiz" and total_quizzes >= 1:
            should_unlock = True
        elif badge.code == "quiz_master" and has_perfect:
            should_unlock = True
        elif badge.code == "streak_3" and user.streak_count >= 3:
            should_unlock = True
        elif badge.code == "streak_7" and user.streak_count >= 7:
            should_unlock = True
        elif badge.code == "xp_100" and user.total_xp >= 100:
            should_unlock = True
        elif badge.code == "xp_500" and user.total_xp >= 500:
            should_unlock = True
        elif badge.code == "pro_learner" and user.is_pro:
            should_unlock = True

        if should_unlock:
            ub = UserBadge(user_id=user.id, badge_id=badge.id)
            db.add(ub)
            unlocked_codes.append(badge.code)

    if unlocked_codes:
        db.commit()
        db.refresh(user)
    return unlocked_codes

def get_daily_quota(db: Session, user: User) -> Tuple[int, int]:
    today = date.today()
    quota = db.query(DailyQuota).filter(
        DailyQuota.user_id == user.id, DailyQuota.date == today
    ).first()
    if not quota:
        quota = DailyQuota(user_id=user.id, date=today, message_count=0, quiz_count=0)
        db.add(quota)
        db.commit()
        db.refresh(quota)
    return quota.message_count, quota.quiz_count

def increment_daily_message(db: Session, user: User):
    today = date.today()
    quota = db.query(DailyQuota).filter(
        DailyQuota.user_id == user.id, DailyQuota.date == today
    ).first()
    if not quota:
        quota = DailyQuota(user_id=user.id, date=today, message_count=1, quiz_count=0)
        db.add(quota)
    else:
        quota.message_count += 1
    db.commit()

def increment_daily_quiz(db: Session, user: User):
    today = date.today()
    quota = db.query(DailyQuota).filter(
        DailyQuota.user_id == user.id, DailyQuota.date == today
    ).first()
    if not quota:
        quota = DailyQuota(user_id=user.id, date=today, message_count=0, quiz_count=1)
        db.add(quota)
    else:
        quota.quiz_count += 1
    db.commit()

def compute_weak_areas(db: Session, user_id: int) -> List[Dict[str, Any]]:
    results = (
        db.query(
            QuizAttempt.topic_title,
            func.avg(QuizAttempt.percentage).label("avg_score"),
            func.count(QuizAttempt.id).label("attempt_count")
        )
        .filter(QuizAttempt.user_id == user_id)
        .group_by(QuizAttempt.topic_title)
        .all()
    )
    
    weak_areas = []
    for r in results:
        if r.avg_score < 75.0:
            weak_areas.append({
                "topic_title": r.topic_title,
                "avg_score": round(r.avg_score, 1),
                "attempt_count": r.attempt_count
            })
    return sorted(weak_areas, key=lambda x: x["avg_score"])
