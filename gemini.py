from __future__ import annotations

from typing import Optional

from google import genai
from google.genai.types import GenerateContentConfig

from config import settings


class GeminiClient:
    """
    Professional Gemini AI Client.

    Responsibilities:
    - Connect Gemini API
    - Generate AI responses
    - Handle configuration
    - Provide safe AI calls
    """

    def __init__(self) -> None:
        self.client: Optional[genai.Client] = None
        self.model = settings.GEMINI_MODEL


    def _initialize_client(self) -> None:
        """
        Lazy Gemini client initialization.
        """

        if self.client:
            return


        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing."
            )


        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )


    def is_ready(self) -> bool:
        """
        Check API key availability.
        """

        return bool(
            settings.GEMINI_API_KEY
        )


    def _build_config(
        self,
        *,
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
    ) -> GenerateContentConfig:

        return GenerateContentConfig(
            system_instruction=system_instruction,

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
        Generate response from Gemini.
        """

        if not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )


        self._initialize_client()


        config = self._build_config(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )


        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )


            if not response:
                return ""


            text = getattr(
                response,
                "text",
                None
            )


            if text:
                return text.strip()


            return ""


        except Exception as error:

            raise RuntimeError(
                f"Gemini generation failed: {error}"
            ) from error



    def safe_generate(
        self,
        prompt: str,
        *,
        system_instruction: Optional[str] = None,
    ) -> str:
        """
        Crash-safe Gemini generation.
        """

        try:

            return self.generate(
                prompt,
                system_instruction=system_instruction,
            )

        except Exception:

            return ""



    def health_check(self) -> bool:
        """
        Verify Gemini API working.
        """

        if not self.is_ready():
            return False


        try:

            response = self.generate(
                "Reply only with OK"
            )

            return (
                response.strip().upper()
                == "OK"
            )


        except Exception:

            return False



# Singleton Gemini Client
gemini_client = GeminiClient()
