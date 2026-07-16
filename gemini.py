from typing import Optional

from google import genai
from google.genai.types import GenerateContentConfig

from config import settings


class GeminiClient:
    """
    Professional Gemini API Client.

    Responsibilities:
    - Initialize Gemini client
    - Validate API key
    - Generate AI responses
    - Health check
    """

    def __init__(self) -> None:

        if not settings.GEMINI_API_KEY.strip():
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    def health_check(self) -> bool:
        """
        Verify that Gemini client
        is initialized correctly.
        """

        return self.client is not None

    def generate(
        self,
        prompt: str,
        *,
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate response from Gemini.
        """

        config = GenerateContentConfig(
            temperature=(
                temperature
                if temperature is not None
                else settings.TEMPERATURE
            ),
            max_output_tokens=(
                max_output_tokens
                if max_output_tokens is not None
                else settings.MAX_OUTPUT_TOKENS
            ),
            system_instruction=system_instruction,
        )

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )

            if response is None:
                return ""

            if getattr(response, "text", None):
                return response.text.strip()

            return ""

        except Exception as error:

            raise RuntimeError(
                f"Gemini request failed: {error}"
            ) from error
          import json
from typing import Any


class GeminiClient:
    ...
    # Part 1 में लिखी गई methods यहीं रहेंगी
    # (__init__, health_check, generate)


    def safe_generate(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
    ) -> str:
        """
        Safe wrapper around generate().
        Never raises an exception.
        """

        try:
            return self.generate(
                prompt=prompt,
                system_instruction=system_instruction,
            )

        except Exception as error:

            return f"Generation Error: {error}"


    def generate_json(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
    ) -> dict[str, Any]:
        """
        Generate JSON response from Gemini.
        """

        response = self.generate(
            prompt=prompt,
            system_instruction=system_instruction,
        )

        try:
            return json.loads(response)

        except json.JSONDecodeError:

            return {
                "success": False,
                "raw_response": response,
                "error": "Invalid JSON returned by Gemini.",
            }


    def validate_response(
        self,
        response: str,
    ) -> bool:
        """
        Validate Gemini response.
        """

        if response is None:
            return False

        if not isinstance(response, str):
            return False

        if not response.strip():
            return False

        return True


    def ping(self) -> bool:
        """
        Simple API connectivity check.
        """

        try:

            result = self.generate(
                "Reply with only the word: OK"
            )

            return "OK" in result.upper()

        except Exception:

            return False
