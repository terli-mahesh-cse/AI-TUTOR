# 🎓 AI-Tutor — Next-Gen AI Tutoring & Assessment Platform

[![Live Demo](https://img.shields.io/badge/Live_Website-ai--tutor--vxl7.onrender.com-4F46E5?style=for-the-badge&logo=render&logoColor=white)](https://ai-tutor-vxl7.onrender.com/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Anthropic Claude](https://img.shields.io/badge/AI-Claude_3.5_Sonnet-D97706?style=for-the-badge&logo=anthropic&logoColor=white)](https://www.anthropic.com/)
[![TailwindCSS](https://img.shields.io/badge/Frontend-TailwindCSS_%2B_Alpine.js-38B2AC?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)

> **Live Application URL**: 🌐 **[https://ai-tutor-vxl7.onrender.com](https://ai-tutor-vxl7.onrender.com/)**

**AI-Tutor** is a modern, full-stack educational web application designed to replace passive video lectures with **active, personalized, 1-on-1 Socratic learning**. Powered by Anthropic's **Claude 3.5 Sonnet**, the platform guides students step-by-step through complex concepts in mathematics, computer science, natural sciences, languages, and standardized test preparation.

---

## 🌟 Live Website Uses & Applications

AI-Tutor is engineered for diverse learning scenarios across students, self-taught developers, and educators:

| Use Case | How AI-Tutor Solves It |
| :--- | :--- |
| **📐 Mathematics & Calculus** | Renders dynamic LaTeX equations ($$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$). Instead of just giving the answer, the tutor asks guiding questions to help you spot algebraic patterns and derivations. |
| **💻 Coding & Algorithms** | Syntax-highlighted code blocks (Python, JavaScript, SQL). Guides learners through debugging logic, Big-O analysis, and data structure trade-offs without spoiling solutions. |
| **🔬 Natural Sciences** | Physics mechanics, chemistry bonding, and cellular biology breakdowns with intuitive real-world analogies. |
| **🌍 Language Learning** | Conversational Spanish, French tense nuances, and Japanese grammar drills with real-time feedback on errors. |
| **🎯 Exam Prep (SAT / GRE / MCAT)** | Rapid test practice, high-yield concept review, and targeted remediation on trick questions. |
| **👨‍👩‍👧 Parent & Teacher Oversight** | Students can generate a secure, read-only **Parent Share Link** allowing parents/educators to inspect study streaks, quiz averages, and weak spots. |

---

## 🚀 Key Features

### 1. Socratic AI Tutoring Workspace
- **Real-time Streaming**: Claude streams responses token-by-token using Server-Sent Events (SSE).
- **Socratic Mode Toggle Switch**:
  - **ON (Socratic)**: The tutor never blurts out the final answer; it asks targeted guiding questions to lead you to eureka moments.
  - **OFF (Direct)**: Provides step-by-step worked examples and first-principle explanations.
- **Rich Media Rendering**: Built-in **KaTeX** for mathematical formulas and **Highlight.js** for code syntax highlighting.
- **Adaptive Feedback**: When you provide an incorrect response, the tutor explains *why* the logic was flawed rather than simply saying "Incorrect".

### 2. Instant Claude AI Quiz Engine
- **On-Demand Generation**: Generates 5 structured conceptual multiple-choice questions on any topic in seconds.
- **Interactive Step Stepper**: Smooth animated slide transitions between questions.
- **Instant Answer Feedback**:
  - 🟢 **Green pulse** for correct choices with immediate confirmation.
  - 🔴 **Red shake** for incorrect choices with step-by-step explanations below.
- **Confetti Celebrations**: Passing score (70%+) triggers a celebratory `canvas-confetti` animation.

### 3. Progress Tracking & Gamification
- **Learning Streaks**: Daily streak counter with flame animation to keep learners accountable.
- **XP & Level Progression**: Earn +20 XP per quiz attempt and +5 XP per correct answer to level up your student rank.
- **Performance Line Chart**: Interactive **Chart.js** graph displaying quiz score trends over time.
- **28-Day Activity Heatmap**: GitHub-style contribution grid tracking daily study sessions.
- **Automated Weak Areas Detection**: Dynamically identifies topics where quiz averages fall below 75% and provides direct one-click practice links.
- **Achievement Badges**: Unlock milestones (*First Steps*, *Quiz Master*, *On Fire*, *Centurion*, etc.) with pop-in modal gallery.

### 4. Subscription & Billing (Stripe)
- **Free Tier**: 10 tutor messages/day, 2 AI quizzes/day, access to all 5 core subjects.
- **Pro Tier ($9.99/mo)**: Unlimited streaming chat, unlimited custom quizzes, and advanced analytics.
- **Stripe Integration**: Stripe Checkout session creation + webhook sync with instant fallback demo upgrade.

### 5. Parent / Teacher Read-Only View
- Secure route `/parent/<share_token>` allowing parents or teachers to view student performance metrics without edit permissions or requiring an account.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11, [FastAPI](https://fastapi.tiangolo.com/), Uvicorn (ASGI)
- **Frontend Architecture**: Jinja2 Templates, [HTMX](https://htmx.org/) (Server-Sent Events), [Alpine.js](https://alpinejs.dev/), [TailwindCSS](https://tailwindcss.com/)
- **UI Libraries**: Lucide Icons, Highlight.js, KaTeX, Chart.js, Canvas-Confetti
- **Database**: [SQLAlchemy](https://www.sqlalchemy.org/) ORM with automatic PostgreSQL support and local SQLite fallback
- **AI Engine**: Anthropic Claude API (`claude-3-5-sonnet-20241022`)
- **Payments**: Stripe API & Webhooks
- **Production Hosting**: [Render.com](https://render.com/) (Web Service + Continuous GitHub Deployment)

---

## 📖 How to Use the Live Website

1. **Visit the Live Site**: Open **[https://ai-tutor-vxl7.onrender.com/](https://ai-tutor-vxl7.onrender.com/)**.
2. **Create an Account**: Click **Get Started Free** and register with your name, email, and password.
3. **Explore Subjects**:
   - Navigate to **Subjects** in the top navbar.
   - Choose from **Math**, **Coding**, **Languages**, **Science**, or **Test Prep**.
4. **Chat with the Tutor**:
   - Click **Start Tutor Chat** on any lesson.
   - Ask any question, test code, or request a step-by-step breakdown.
   - Toggle **Socratic Mode** ON/OFF in the top-right header to switch tutoring styles.
5. **Take an AI Quiz**:
   - Click **Take Quiz** or **Quizzes** in the navbar.
   - Click **Generate 5-Question Quiz** and test your conceptual understanding.
6. **Review Your Dashboard**:
   - Check your streak, total XP, score chart, and weak areas under **Dashboard**.
   - Click your profile to access your **Parent Share Link**.

---

## 💻 Running Locally (Windows / macOS / Linux)

### Quick Start on Windows (One-Click Launcher)
If you have cloned this repository locally on Windows:
- Simply double-click **`START_AI_TUTOR.bat`** (or **`run.bat`**).
- It will automatically verify the database, start the FastAPI server, and open `http://localhost:8000` in your browser!

### Manual Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/terli-mahesh-cse/AI-TUTOR.git
   cd AI-TUTOR
   ```

2. **Create a virtual environment & install dependencies**:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Add your Anthropic API Key in `.env`:
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

4. **Seed the database**:
   ```bash
   python seed.py
   ```

5. **Start the server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## 📂 Project Structure

```
AI-TUTOR/
├── app/
│   ├── main.py                 # FastAPI application entrypoint & health checks
│   ├── config.py               # Settings via pydantic-settings (.env reader)
│   ├── database.py             # SQLAlchemy engine & session factory
│   ├── models/                 # Database models (User, Subject, Lesson, QuizAttempt, etc.)
│   ├── schemas/                # Pydantic validation schemas
│   ├── routers/
│   │   ├── auth.py             # Signup, login, logout, JWT cookies
│   │   ├── chat.py             # Streaming chat endpoint (SSE)
│   │   ├── quiz.py             # Claude quiz generator & submission
│   │   ├── dashboard.py        # Analytics, XP, heatmaps, weak areas
│   │   ├── subjects.py         # Curriculum library
│   │   ├── parent.py           # Read-only student share view
│   │   └── billing.py          # Stripe Checkout & webhooks
│   ├── services/
│   │   ├── claude_client.py    # Anthropic Claude streaming wrapper
│   │   ├── tutor_prompts.py    # Socratic and direct tutoring personas
│   │   ├── quiz_generator.py   # Claude structured JSON quiz builder
│   │   └── progress_tracker.py # Streaks, XP calculations, badges
│   └── templates/              # Jinja2 HTML templates
│       ├── base.html           # Dark mode, responsive navbar, CDNs
│       ├── landing.html        # Hero, features, subject carousel, pricing
│       ├── chat.html           # Real-time token streaming chat interface
│       ├── quiz.html           # Animated question stepper & confetti
│       ├── dashboard.html      # Chart.js trend graphs & activity heatmap
│       ├── subjects.html       # SVG circular progress curriculum cards
│       ├── parent_dashboard.html # Read-only student report
│       └── auth/               # Login and signup templates
├── alembic/                    # Database migrations
├── seed.py                     # Initial database seeder script
├── Dockerfile                  # Container deployment configuration
├── render.yaml                 # Render.com deployment Blueprint
├── requirements.txt            # Pinned Python dependencies
├── START_AI_TUTOR.bat          # Windows one-click local launcher
└── README.md                   # Project documentation
```

---

## 🛡️ License

This project is open-source and available under the [MIT License](LICENSE).
