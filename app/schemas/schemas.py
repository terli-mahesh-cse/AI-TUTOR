from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_pro: bool
    streak_count: int
    total_xp: int
    parent_share_token: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class SubjectResponse(BaseModel):
    id: int
    name: str
    slug: str
    icon: str
    description: str
    color: str

    class Config:
        from_attributes = True

class LessonResponse(BaseModel):
    id: int
    subject_id: int
    title: str
    slug: str
    summary: str
    order: int
    initial_prompt: str

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    content: str
    subject_id: Optional[int] = None
    lesson_id: Optional[int] = None
    is_socratic: bool = False

class MessageResponse(BaseModel):
    id: int
    sender: str
    content: str
    is_socratic: bool
    created_at: datetime

    class Config:
        from_attributes = True

class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_index: int
    explanation: str

class QuizSubmit(BaseModel):
    topic_title: str
    subject_id: Optional[int] = None
    lesson_id: Optional[int] = None
    answers: List[int]  # selected option index for each question
    questions: List[QuizQuestion]

class QuizResultResponse(BaseModel):
    score: int
    total: int
    percentage: float
    xp_earned: int
    passed: bool
    unlocked_badges: List[str]
