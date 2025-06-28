import os
from typing import Optional
from openai import OpenAI


class Generator:

    def __init__(
        self,
        base_url: str = "https://xiaohumini.site/v1",
        api_key: str = os.getenv("OPENAI_API_KEY"),
        default_model: str = "gemini-2.5-flash-lite-preview-06-17",
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.default_model = default_model

    def generate_response(self, messages: list, model: Optional[str] = None) -> str:
        if model is None:
            model = self.default_model
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content

    def generate_with_default_messages(
        self, user_content: str, model: Optional[str] = None
    ) -> str:
        if model is None:
            model = self.default_model
        messages = [
            {
                "role": "system",
                "content": "You are a human.",
            },
            {
                "role": "user",
                "content": user_content,
            },
        ]
        return self.generate_response(messages, model)
