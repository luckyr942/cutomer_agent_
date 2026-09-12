import os
import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0,str(ROOT_DIR))


# pyrefly: ignore [missing-import]
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    DEFAULT_MODEL,
)


class LLMClient:
    """OpenAI API wrapper with dallback support for offline/mock responses."""

    def __init__(
        self,
        api_key: str = OPENAI_API_KEY,
        base_url: str = OPENAI_BASE_URL,
        model: str = DEFAULT_MODEL,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                default_headers={
                    "HTTP-Referer": "https://github.com/customer-support-agent",
                    "X-Title": "Customer Support Agent",
                },
            )
        else:
            self.client = None
            
    def generate(self, prompt: str, system_prompt: str = "You are a helpful customer support AI assistant.") -> str:
        """Sends a completion request to LLM API (or mock if no key is present)."""

        if not self.client:
            print("No API KEYS are found ")
            return self._mock_response(prompt)

        try:
            response = self.client.chat.completions.create(
                model = self.model,
                messages = [
                    {   "role" : "system",
                        "content" :system_prompt,
                    },
                    {
                        "role": "user",
                        "content" : prompt,
                    },
                ],
                temperature=0.2,
                max_tokens=300
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("LLM returned an empty response.")

            return content.strip()

        except Exception as error:
            print(
                f"LLM API call failed: {error}"
            )
            print("Falling back to mock response.")

            return self._mock_response(prompt)

    
    def _mock_response(self, prompt: str) -> str:
        """
        Offline fallback used when the API is unavailable.
        """

        prompt_lower = prompt.lower()

        if "json" in prompt_lower or "classify" in prompt_lower:
            return json.dumps(
                {
                    "intent": "delivery_delay",
                    "confidence": 0.95,
                    "reasoning": (
                        "Customer asked about package "
                        "delivery status."
                    ),
                }
            )

        return (
            "Thank you for reaching out! "
            "We are looking into your request "
            "and will assist you shortly."
        )


if __name__ == "__main__":
    llm = LLMClient()

    response = llm.generate(
        "Hello, where is my order #12345?"
    )

    print("\n=== LLM RESPONSE ===")
    print(response)
            
        
        