import os
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, get_db
from app.models.models import User
from app.routers import auth, chat, quiz, dashboard, subjects, parent, billing
from app.routers.auth import get_current_user_optional
from seed import seed_database

# Create database tables automatically
Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# Mount Static Files
os.makedirs("app/static/css", exist_ok=True)
os.makedirs("app/static/js", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Include Routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(dashboard.router)
app.include_router(subjects.router)
app.include_router(parent.router)
app.include_router(billing.router)

@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
def landing_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    return templates.TemplateResponse(request=request, name="landing.html", context={"user": user})

@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
