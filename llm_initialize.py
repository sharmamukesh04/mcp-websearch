import os
import httpx
from mcp_agent.workflows.llm.augmented_llm import AugmentedLLM, RequestParams
from dotenv import load_dotenv

load_dotenv()

class GroqAugmentedLLM(AugmentedLLM):
    async def generate(self, messages, request_params: RequestParams):
        """Handles chat-based multi-message inputs (OpenAI-style)."""
        return await self._call_groq_api(messages)

    async def generate_structured(self, messages, schema, request_params: RequestParams):
        """Return raw response as a dict for structured LLM output. (Basic support)"""
        result = await self._call_groq_api(messages)
        return {"response": result}

    async def generate_str(self, message: str, request_params: RequestParams = RequestParams()):
        """Helper for single-message string input."""
        messages = [{"role": "user", "content": message}]
        return await self._call_groq_api(messages)

    async def _call_groq_api(self, messages):
        groq_key = os.getenv("GROQ_API")
        model_name = os.getenv("MODEL_NAME", "deepseek-r1-distill-llama-70b")

        if not groq_key:
            raise ValueError("GROQ_API_KEY not set in environment")

        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": 0.3,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
