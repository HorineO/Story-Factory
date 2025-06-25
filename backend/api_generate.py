from openai import OpenAI


class OpenAIGenerator:
    def __init__(
        self,
        base_url: str = "https://xiaohumini.site/v1",
        api_key: str = "sk-8mP2ANPxanMXHYQ0GQHQVJkeqTiU2iWoSu9lvt00SR8wjKHS",
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def generate_response(self, model: str, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content

    def generate_with_default_messages(self, model: str, user_content: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a coding assistant that talks like a pirate.",
            },
            {
                "role": "user",
                "content": user_content,
            },
        ]
        return self.generate_response(model, messages)
