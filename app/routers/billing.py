import stripe
from fastapi import APIRouter, Depends, Request, HTTPException, Header
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.models import User
from app.routers.auth import get_current_user
from app.services.progress_tracker import check_and_award_badges

stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(prefix="/billing", tags=["billing"])
templates = Jinja2Templates(directory="app/templates")

@router.get("", response_class=HTMLResponse)
def billing_page(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="billing.html", context={"user": user})

@router.post("/create-checkout-session")
def create_checkout_session(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    domain_url = str(request.base_url).rstrip("/")

    if not settings.STRIPE_SECRET_KEY:
        # Development fallback upgrade toggle if Stripe secret key is not set
        user.is_pro = True
        db.commit()
        db.refresh(user)
        check_and_award_badges(db, user)
        return RedirectResponse(url="/billing/success?demo=true", status_code=303)

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=user.email,
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "AI-Tutor Pro Subscription",
                            "description": "Unlimited AI tutor streaming chat, unlimited custom topic quizzes & advanced analytics.",
                        },
                        "unit_amount": 999,  # $9.99
                        "recurring": {"interval": "month"},
                    },
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=f"{domain_url}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{domain_url}/billing/cancel",
            metadata={"user_id": str(user.id)}
        )
        return RedirectResponse(url=checkout_session.url, status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db), stripe_signature: str = Header(None)):
    payload = await request.body()
    event = None

    if not settings.STRIPE_WEBHOOK_SECRET:
        return JSONResponse(content={"status": "Stripe webhook secret not configured"}, status_code=200)

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook Error: {str(e)}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("metadata", {}).get("user_id")
        if user_id:
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                user.is_pro = True
                db.commit()
                check_and_award_badges(db, user)

    return JSONResponse(content={"status": "success"}, status_code=200)

@router.get("/success", response_class=HTMLResponse)
def billing_success(request: Request, demo: bool = False, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user.is_pro = True
    db.commit()
    check_and_award_badges(db, user)
    return templates.TemplateResponse(request=request, name="billing_success.html", context={"user": user, "demo": demo})

@router.get("/cancel", response_class=HTMLResponse)
def billing_cancel(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="billing_cancel.html", context={"user": user})
