import asyncio
from typing import AsyncGenerator, List, Dict
import anthropic
from app.config import settings

class ClaudeClient:
    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY
        self.model = settings.CLAUDE_MODEL
        if self.api_key:
            self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
        else:
            self.client = None

    async def stream_chat_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """
        Yields text chunks as they arrive from Claude API.
        If no API key is provided, falls back to a smart mock stream.
        """
        if not self.client:
            # Fallback smart mock response for testing without API key
            last_msg = messages[-1]["content"].lower() if messages else ""
            
            if any(k in last_msg for k in ["python", "code", "list", "print", "function", "variable"]):
                mock_reply = (
                    "Hello! Let's look at this coding concept. Here is an example of what you're asking about:\n\n"
                    "```python\n"
                    "# Let's define a function to solve this\n"
                    "def process_data(items):\n"
                    "    for item in items:\n"
                    "        print(f'Processing {item}')\n"
                    "```\n\n"
                    "To understand this, what do you think is the role of the loop in the function above?"
                )
            elif any(k in last_msg for k in ["solve", "equation", "math", "limit", "derivative", "x", "+", "-", "*", "/"]):
                mock_reply = (
                    "Hello! Let's explore this mathematical problem step by step.\n\n"
                    "Consider the equation or rule you mentioned. We can represent it as:\n"
                    "$$f(x) = x^2 + 2x - 3$$\n\n"
                    "First, what is the derivative $f'(x)$ of this function, or how would you simplify it? Give it a try!"
                )
            else:
                last_msg_clean = messages[-1]["content"] if messages else "your query"
                mock_reply = (
                    f"Hello! I am your AI Socratic Tutor. Let's analyze your question: \"{last_msg_clean}\".\n\n"
                    "To help you build the right intuition, let's break this down:\n"
                    "1. What is the core definition or rule that applies here?\n"
                    "2. What information do we already have, and what is missing?\n\n"
                    "What do you think is the very first step we should take to explore this?"
                )

            for word in mock_reply.split(" "):
                yield word + " "
                await asyncio.sleep(0.04)
            return

        try:
            async with self.client.messages.stream(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=messages
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as e:
            yield f"\n[Error communicating with Claude API: {str(e)}]"

    async def generate_json(self, system_prompt: str, prompt: str) -> str:
        """
        Calls Claude to return a JSON string (used for quiz generation).
        """
        if not self.client:
            # Fallback mock quiz JSON for testing
            return """[
                {
                    "id": 1,
                    "question": "What is the primary purpose of solving an algebraic equation?",
                    "options": ["To find the unknown variable value that makes the equation true", "To memorize formulas", "To eliminate numbers", "To graph a straight line only"],
                    "correct_index": 0,
                    "explanation": "Solving an equation means finding the value(s) of the variable that satisfy the equation equality."
                },
                {
                    "id": 2,
                    "question": "If 2x + 6 = 14, what is the value of x?",
                    "options": ["2", "4", "6", "8"],
                    "correct_index": 1,
                    "explanation": "Subtract 6 from both sides to get 2x = 8, then divide by 2 to get x = 4."
                },
                {
                    "id": 3,
                    "question": "Which property allows us to multiply both sides of an equation by the same non-zero number?",
                    "options": ["Multiplication Property of Equality", "Distributive Property", "Associative Property", "Commutative Property"],
                    "correct_index": 0,
                    "explanation": "The Multiplication Property of Equality states that if a = b, then a * c = b * c."
                },
                {
                    "id": 4,
                    "question": "What happens when an equation results in 0 = 0?",
                    "options": ["There is no solution", "There are infinitely many solutions", "The variable is 0", "The equation is invalid"],
                    "correct_index": 1,
                    "explanation": "An identity like 0 = 0 means the equation is true for all values of the variable (infinitely many solutions)."
                },
                {
                    "id": 5,
                    "question": "What is the solution set to |x - 3| = 5?",
                    "options": ["x = 8 or x = -2", "x = 8 only", "x = -8 or x = 2", "x = 5 or x = -5"],
                    "correct_index": 0,
                    "explanation": "Break into two cases: x - 3 = 5 (x = 8) and x - 3 = -5 (x = -2)."
                }
            ]"""

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

claude_client = ClaudeClient()
