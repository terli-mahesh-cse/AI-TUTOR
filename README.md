# 🎓 AI-Tutor — AI-Powered Tutoring & Assessment Platform

AI-Tutor is a full-stack, single-platform deployable Python application built with **FastAPI**, **Jinja2 + HTMX + Alpine.js + TailwindCSS**, **SQLAlchemy & PostgreSQL**, **Anthropic Claude 3.5 Sonnet API**, and **Stripe Checkout**.

---

## 🚀 Key Features

1. **Socratic AI Tutoring Workspace**:
   - Real-time token streaming via Server-Sent Events (SSE).
   - Socratic Mode toggle switch (asks guiding questions instead of direct solutions).
   - Code block syntax highlighting (**Highlight.js**) and LaTeX math equation rendering (**KaTeX**).
   - Daily free tier quota enforcement (10 messages/day).

2. **Instant Claude AI Quiz Generator**:
   - Generates 5 structured multiple-choice questions on any topic in real-time.
   - Interactive single-question step stepper UI with instant green pulse / red shake feedback and step-by-step explanations.
   - Confetti score celebration (`canvas-confetti`) on passing grade (70%+).

3. **Curriculum & Subject Library**:
   - 5 pre-seeded learning tracks: **Math**, **Coding**, **Natural Sciences**, **World Languages**, **Test Prep**.
   - SVG circular progress rings and topic completion checkmarks.

4. **Gamification & Analytics Dashboard**:
   - Streak counter with animated flame icon.
   - Leveling system (+20 XP attempt, +5 XP correct answer).
   - Interactive **Chart.js** quiz performance trend graph.
   - 28-Day GitHub-style activity contribution heatmap grid.
   - Auto-derived **Weak Areas** remediation links.
   - Achievement Badge gallery pop-in modal (`First Steps`, `Quiz Master`, `On Fire`, `Centurion`, etc.).

5. **Parent / Teacher Progress Link**:
   - Unique read-only share token route `/parent/<share_token>` allowing parents to inspect student performance without editing rights.

6. **Stripe Subscription Billing**:
   - Free Tier vs Pro Tier ($9.99/mo).
   - Stripe Checkout session creation + webhook handler.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Database**: PostgreSQL (SQLAlchemy ORM + Alembic migrations, with automatic SQLite fallback for zero-config local dev)
- **Frontend**: Jinja2 HTML Templates, HTMX, Alpine.js, TailwindCSS CDN, Lucide Icons, Highlight.js, KaTeX, Chart.js, Canvas-Confetti
- **AI Integration**: Anthropic Claude API (`claude-3-5-sonnet-20241022`)
- **Payments**: Stripe API & Webhooks
- **Deployment**: Render.com single web service (`render.yaml`)

---

## ⚙️ Local Setup Instructions

### 1. Clone & Install Dependencies
```bash
cd AI-TUTOR
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

### 2. Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your API keys in `.env` if available:
- `ANTHROPIC_API_KEY`: Your Anthropic API key (optional for local testing; smart fallback stream included if omitted)
- `STRIPE_SECRET_KEY` & `STRIPE_WEBHOOK_SECRET`: Stripe API credentials (optional; demo upgrade toggle included if omitted)

### 3. Seed Database
Run the seed script to populate sample subjects, lessons, and badges:
```bash
python seed.py
```

### 4. Run Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
Open your browser at [http://localhost:8000](http://localhost:8000).

---

## ☁️ Deploying to Render.com

This repository is pre-configured with `render.yaml` for a single-click deployment:

1. Push this repository to GitHub/GitLab.
2. Go to [Render Dashboard](https://dashboard.render.com/) and click **New +** -> **Blueprint**.
3. Connect your repository. Render will automatically detect `render.yaml` and configure:
   - **Web Service**: Python FastAPI application (`uvicorn app.main:app`)
   - **PostgreSQL Database**: Managed Postgres addon (`ai-tutor-db`)
4. Add your production environment variables (`ANTHROPIC_API_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`) in the Render Web Service settings.
5. Deploy!

---

## 📄 Project Structure

```
ai-tutor/
├── app/
│   ├── main.py                 # FastAPI application entrypoint
│   ├── config.py               # Settings via pydantic-settings
│   ├── database.py             # SQLAlchemy engine & session factory
│   ├── models/                 # SQLAlchemy models (User, Subject, Lesson, Message, QuizAttempt, etc.)
│   ├── schemas/                # Pydantic schemas
│   ├── routers/                # Endpoint routers (auth, chat, quiz, dashboard, subjects, parent, billing)
│   ├── services/               # Services (claude_client, tutor_prompts, quiz_generator, progress_tracker)
│   ├── templates/              # Jinja2 HTML templates & partials
│   └── static/                 # Static asset folders
├── alembic/                    # Database migrations
├── seed.py                     # Database seeding script
├── render.yaml                 # Render single-service configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Sample environment file
└── README.md                   # Documentation
```
