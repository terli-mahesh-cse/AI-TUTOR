from app.database import engine, SessionLocal, Base
from app.models.models import Subject, Lesson, Badge

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check existing subjects
        if db.query(Subject).first():
            print("Database already seeded.")
            return

        subjects_data = [
            {
                "name": "Math",
                "slug": "math",
                "icon": "calculator",
                "description": "Master algebra, calculus, geometry, and problem-solving step by step.",
                "color": "indigo",
                "lessons": [
                    {
                        "title": "Algebraic Equations & Inequalities",
                        "slug": "algebraic-equations",
                        "summary": "Learn to solve linear equations, quadratic equations, and absolute value inequalities.",
                        "order": 1,
                        "initial_prompt": "Hi! I'd like to learn how to solve algebraic equations step by step."
                    },
                    {
                        "title": "Limits & Derivatives in Calculus",
                        "slug": "limits-derivatives",
                        "summary": "Understand the intuition of rate of change, limits definition, and power rule derivatives.",
                        "order": 2,
                        "initial_prompt": "Help me understand limits and how derivatives measure instantaneous change."
                    },
                    {
                        "title": "Pythagorean Theorem & Trigonometry",
                        "slug": "trigonometry-basics",
                        "summary": "Explore right-triangle geometry, sine, cosine, tangent, and unit circle concepts.",
                        "order": 3,
                        "initial_prompt": "Teach me how sine, cosine, and tangent relate to right triangles and the unit circle."
                    },
                    {
                        "title": "Probability & Statistics",
                        "slug": "probability-stats",
                        "summary": "Mean, median, mode, standard deviation, and basic probability theory.",
                        "order": 4,
                        "initial_prompt": "Let's learn probability and how to calculate variance and standard deviation."
                    }
                ]
            },
            {
                "name": "Coding",
                "slug": "coding",
                "icon": "code",
                "description": "Build real projects in Python, JavaScript, Algorithms, and System Design.",
                "color": "emerald",
                "lessons": [
                    {
                        "title": "Python Data Structures",
                        "slug": "python-data-structures",
                        "summary": "Master Lists, Dictionaries, Sets, Tuples, and list comprehensions in Python.",
                        "order": 1,
                        "initial_prompt": "Guide me through Python lists, dictionaries, and sets with real code examples."
                    },
                    {
                        "title": "Algorithms: Big-O & Searching",
                        "slug": "algorithms-big-o",
                        "summary": "Analyze time and space complexity, binary search, and recursion.",
                        "order": 2,
                        "initial_prompt": "Explain Big-O notation and how binary search works with code examples."
                    },
                    {
                        "title": "Web Development Basics",
                        "slug": "web-dev-basics",
                        "summary": "Build structured HTML markup, responsive CSS flexbox/grid, and JavaScript DOM manipulation.",
                        "order": 3,
                        "initial_prompt": "Show me how HTML, CSS, and JS interact to build interactive web pages."
                    },
                    {
                        "title": "SQL Databases & Queries",
                        "slug": "sql-databases",
                        "summary": "Learn SELECT queries, JOINs, GROUP BY aggregations, and database normalization.",
                        "order": 4,
                        "initial_prompt": "Teach me SQL queries, INNER JOINs vs LEFT JOINs, and database design."
                    }
                ]
            },
            {
                "name": "Languages",
                "slug": "languages",
                "icon": "languages",
                "description": "Practice conversational fluency, grammar patterns, and vocabulary in Spanish, French & more.",
                "color": "amber",
                "lessons": [
                    {
                        "title": "Spanish Conversational Basics",
                        "slug": "spanish-conversational",
                        "summary": "Greetings, essential verbs (ser vs estar), and ordering food in Spanish.",
                        "order": 1,
                        "initial_prompt": "Practice a friendly Spanish conversation with me and correct my grammar as we speak!"
                    },
                    {
                        "title": "French Present & Past Tenses",
                        "slug": "french-tenses",
                        "summary": "Master Passé Composé vs Imparfait with practical conversational examples.",
                        "order": 2,
                        "initial_prompt": "Explain when to use Passé Composé versus Imparfait in French with examples."
                    },
                    {
                        "title": "Japanese Greetings & Hiragana",
                        "slug": "japanese-hiragana",
                        "summary": "Learn core Japanese sentence structures, particles (wa, ga, o), and polite speech.",
                        "order": 3,
                        "initial_prompt": "Teach me basic Japanese sentence structure and how subject particles work."
                    }
                ]
            },
            {
                "name": "Science",
                "slug": "science",
                "icon": "flask-conical",
                "description": "Explore Newtonian mechanics, organic chemistry reactions, and cellular biology.",
                "color": "rose",
                "lessons": [
                    {
                        "title": "Newton's Laws & Mechanics",
                        "slug": "newtons-laws",
                        "summary": "Inertia, F=ma, action-reaction pairs, and free-body diagram problem solving.",
                        "order": 1,
                        "initial_prompt": "Explain Newton's three laws of motion with real-world physics problems."
                    },
                    {
                        "title": "Cellular Respiration & Photosynthesis",
                        "slug": "cellular-respiration",
                        "summary": "ATP production, glycolysis, Krebs cycle, and light-dependent reactions.",
                        "order": 2,
                        "initial_prompt": "Guide me through cellular respiration, ATP generation, and photosynthesis."
                    },
                    {
                        "title": "Chemical Bonding & Reactions",
                        "slug": "chemical-bonding",
                        "summary": "Ionic vs covalent bonds, electronegativity, VSEPR molecular shapes.",
                        "order": 3,
                        "initial_prompt": "Help me understand covalent vs ionic bonding and molecular geometry."
                    }
                ]
            },
            {
                "name": "Test Prep",
                "slug": "test-prep",
                "icon": "graduation-cap",
                "description": "Targeted practice for SAT Math, GRE Verbal, AP Computer Science, and MCAT.",
                "color": "purple",
                "lessons": [
                    {
                        "title": "SAT Math: High-Yield Problem Strategies",
                        "slug": "sat-math-prep",
                        "summary": "Triangles, linear systems, exponent rules, and quick estimation hacks.",
                        "order": 1,
                        "initial_prompt": "Give me a high-yield SAT Math practice problem and break down the strategy."
                    },
                    {
                        "title": "GRE Vocabulary & Text Completion",
                        "slug": "gre-vocab",
                        "summary": "Master high-frequency GRE words and context clues in complex sentence structures.",
                        "order": 2,
                        "initial_prompt": "Help me practice GRE text completion questions and master advanced vocabulary."
                    }
                ]
            }
        ]

        for s_data in subjects_data:
            lessons_list = s_data.pop("lessons")
            subject = Subject(**s_data)
            db.add(subject)
            db.flush()

            for l_data in lessons_list:
                lesson = Lesson(subject_id=subject.id, **l_data)
                db.add(lesson)

        # Badges
        badges_data = [
            {"code": "first_quiz", "title": "First Steps", "description": "Completed your first topic quiz", "icon": "trophy"},
            {"code": "quiz_master", "title": "Quiz Master", "description": "Scored 100% on any topic quiz", "icon": "award"},
            {"code": "streak_3", "title": "On Fire", "description": "Maintained a 3-day learning streak", "icon": "flame"},
            {"code": "streak_7", "title": "Unstoppable", "description": "Maintained a 7-day learning streak", "icon": "zap"},
            {"code": "xp_100", "title": "Centurion", "description": "Accumulated over 100 total XP", "icon": "star"},
            {"code": "xp_500", "title": "Scholar", "description": "Accumulated over 500 total XP", "icon": "crown"},
            {"code": "pro_learner", "title": "Pro Learner", "description": "Upgraded to AI-Tutor Pro Subscription", "icon": "sparkles"},
        ]

        for b_data in badges_data:
            badge = Badge(**b_data)
            db.add(badge)

        db.commit()
        print("Database seeded successfully with subjects, lessons, and badges!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
