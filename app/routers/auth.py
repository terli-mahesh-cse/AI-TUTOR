from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.config import settings
from app.database import get_db
from app.models.models import User, Badge, UserBadge

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="app/templates")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user_optional(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    token = request.cookies.get("access_token")
    if not token and "Authorization" in request.headers:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    if not token:
        return None
    if token.startswith("Bearer "):
        token = token[7:]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
    except Exception:
        return None

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user = get_current_user_optional(request, db)
    if not user:
        # Check if HTMX request
        if request.headers.get("HX-Request"):
            response = Response(status_code=200)
            response.headers["HX-Redirect"] = "/auth/login"
            raise HTTPException(status_code=401, detail="Unauthorized")
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/auth/login"}
        )
    return user

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(request=request, name="auth/login.html", context={"error": None})

@router.post("/login")
def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email.lower().strip()).first()
    if not user or not verify_password(password, user.hashed_password):
        if request.headers.get("HX-Request"):
            return templates.TemplateResponse(
                request=request,
                name="auth/login.html",
                context={"error": "Invalid email or password", "email": email},
                status_code=400
            )
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"error": "Invalid email or password", "email": email}
        )
    
    token = create_access_token(data={"sub": str(user.id)})
    
    if request.headers.get("HX-Request"):
        res = Response(status_code=200)
        res.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        res.headers["HX-Redirect"] = "/dashboard"
        return res

    redirect_res = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    redirect_res.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return redirect_res

@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(request=request, name="auth/signup.html", context={"error": None})

@router.post("/signup")
def signup(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    email_clean = email.lower().strip()
    existing_user = db.query(User).filter(User.email == email_clean).first()
    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="auth/signup.html",
            context={"error": "An account with this email already exists.", "full_name": full_name, "email": email}
        )

    if len(password) < 6:
        return templates.TemplateResponse(
            request=request,
            name="auth/signup.html",
            context={"error": "Password must be at least 6 characters long.", "full_name": full_name, "email": email}
        )

    user = User(
        email=email_clean,
        full_name=full_name.strip(),
        hashed_password=get_password_hash(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    
    if request.headers.get("HX-Request"):
        res = Response(status_code=200)
        res.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        res.headers["HX-Redirect"] = "/dashboard"
        return res

    redirect_res = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    redirect_res.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return redirect_res

@router.get("/logout")
def logout(response: Response):
    res = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    res.delete_cookie("access_token")
    return res
