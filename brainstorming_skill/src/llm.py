import os
import json
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, provider: str = None):
        self.provider = provider or os.getenv("LLM_PROVIDER", "openai")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-2024-11-20")
        self.api_key = (
            os.getenv("OPENAI_API_KEY") or
            os.getenv("ANTHROPIC_API_KEY") or
            os.getenv("GROK_API_KEY")
        )
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")

    def complete(self, messages: List[Dict], temperature: float = 0.7) -> str:
        if self.provider == "openai":
            return self._openai(messages, temperature)
        elif self.provider == "anthropic":
            return self._anthropic(messages, temperature)
        elif self.provider == "ollama":
            return self._ollama(messages, temperature)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _openai(self, messages, temp):
        import openai
        openai.api_key = self.api_key
        resp = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temp,
            response_format={"type": "json_object"} if "json" in messages[-1].get("content", "") else None
        )
        return resp.choices[0].message.content.strip()

    def _anthropic(self, messages, temp):
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msg = next(m["content"] for m in messages if m["role"] == "user")
        resp = client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=temp,
            system=system,
            messages=[{"role": "user", "content": user_msg}]
        )
        return resp.content[0].text

    def _ollama(self, messages, temp):
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temp,
            "stream": False
        }
        resp = requests.post(f"{self.ollama_url}/api/chat", json=payload)
        resp.raise_for_status()
        return resp.json()["message"]["content"]

# Global LLM client instance
llm = LLMClient()