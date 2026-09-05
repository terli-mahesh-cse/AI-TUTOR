import json
import re
from typing import List, Dict, Any
from app.services.claude_client import claude_client

async def generate_quiz_questions(topic_title: str, subject_name: str = "General") -> List[Dict[str, Any]]:
    system_prompt = """You are an expert educational assessment creator.
Generate a 5-question multiple choice quiz testing deep conceptual understanding of the requested topic.

CRITICAL INSTRUCTIONS:
1. Return ONLY a valid JSON array of 5 question objects.
2. No intro text, no outer markdown formatting if possible, just raw JSON.
3. Format of each question object:
{
  "id": 1,
  "question": "Clear, precise question text (use LaTeX $eq$ if math)",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_index": 0,
  "explanation": "Step-by-step clear explanation why Option A is correct and others are wrong."
}
4. Options MUST be 4 distinct choices.
5. `correct_index` MUST be an integer between 0 and 3.
"""

    user_prompt = f"Generate a 5-question quiz for the topic: '{topic_title}' in the subject: '{subject_name}'."
    
    raw_response = await claude_client.generate_json(system_prompt, user_prompt)
    
    # Clean JSON markdown fences if present
    cleaned = raw_response.strip()
    if "```json" in cleaned:
        match = re.search(r"```json\s*(.*?)\s*```", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1)
    elif "```" in cleaned:
        match = re.search(r"```\s*(.*?)\s*```", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1)

    try:
        data = json.loads(cleaned)
        if isinstance(data, list) and len(data) > 0:
            return data
    except Exception as e:
        print(f"Error parsing quiz JSON from Claude: {e}")

    # Fallback structure if JSON parse failed
    return [
        {
            "id": 1,
            "question": f"What is a fundamental concept in {topic_title}?",
            "options": [
                "Understanding the core principles and definitions",
                "Memorizing random equations without context",
                "Skipping problem-solving practice",
                "Ignoring step-by-step derivation"
            ],
            "correct_index": 0,
            "explanation": "Core principles form the foundation of true understanding."
        },
        {
            "id": 2,
            "question": f"How do you effectively solve problems in {topic_title}?",
            "options": [
                "Guessing randomly",
                "Breaking the problem into logical steps",
                "Skipping the verification phase",
                "Looking up answers immediately"
            ],
            "correct_index": 1,
            "explanation": "Decomposing complex problems into smaller logical steps is the key."
        }
    ]
