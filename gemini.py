from __future__ import annotations

from typing import Optional

from google import genai
from google.genai.types import GenerateContentConfig

from config import settings


class GeminiClient:
    """
    Professional Gemini API Client.

    Responsibilities
    ----------------
    • Initialize Gemini
    • Validate configuration
    • Generate AI responses
    • Health checking
    """

    def __init__(self) -> None:

        self._validate_settings()

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    @staticmethod
    def _validate_settings() -> None:
        """
        Validate required settings.
        """

        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing."
            )

    @property
    def model_name(self) -> str:
        """
        Return active Gemini model.
        """

        return self.model

    def health_check(self) -> bool:
        """
        Verify Gemini client.
        """

        try:
            return self.client is not None

        except Exception:
            return False

    def _build_config(
        self,
        *,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
        system_instruction: Optional[str] = None,
    ) -> GenerateContentConfig:
        """
        Build generation configuration.
        """

        return GenerateContentConfig(
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
            def generate(
        self,
        prompt: str,
        *,
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a text response from Gemini.
        """

        config = self._build_config(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            system_instruction=system_instruction,
        )

        try:

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config,
            )

        except Exception as error:

            raise RuntimeError(
                f"Gemini request failed: {error}"
            ) from error

        if response is None:
            return ""

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        try:

            parts = response.candidates[0].content.parts

            output = []

            for part in parts:

                if hasattr(part, "text") and part.text:
                    output.append(part.text)

            return "\n".join(output).strip()

        except Exception:

            return ""


    def generate_with_system_prompt(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Generate content using
        system instruction.
        """

        return self.generate(
            prompt=user_prompt,
            system_instruction=system_prompt,
        )
            def safe_generate(
        self,
        prompt: str,
        *,
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
    ) -> str:
        """
        Safe wrapper around generate().
        Never raises an exception.
        """

        try:
            return self.generate(
                prompt=prompt,
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            )

        except Exception:
            return ""


    def generate_json(
        self,
        prompt: str,
        *,
        system_instruction: Optional[str] = None,
    ) -> dict:
        """
        Generate and parse JSON response.
        """

        import json

        response = self.safe_generate(
            prompt=prompt,
            system_instruction=system_instruction,
        )

        if not response:
            return {}

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return {
                "raw_response": response
            }


    @staticmethod
    def validate_response(response: str) -> bool:
        """
        Validate AI response.
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
        Test Gemini connectivity.
        """

        try:

            response = self.generate(
                prompt="Reply with only one word: OK"
            )

            return "OK" in response.upper()

        except Exception:
            return False


# Singleton Client
gemini_client = GeminiClient()
