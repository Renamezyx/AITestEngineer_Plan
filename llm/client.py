import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError


class LLMClient:
    def __init__(self):
        load_dotenv()
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("DEEPSEEK_API_KEY 未设置")
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def complete_json(
        self,
        messages: list[dict],
        schema: object | None = None,
        model: str = "deepseek-v4-flash",
        temperature: float = 0.2,
        response_format: dict | None = None,
        max_attempts: int = 2,
    ):
        if response_format is None:
            response_format = {"type": "json_object"}

        result = {
            "usage": {
                "completion_tokens": 0,
                "prompt_tokens": 0,
                "total_tokens": 0,
            },
            "content": None,
            "error": None,
            "success": False,
        }
        history = list(messages)
        last_error = None

        for attempt in range(1, max_attempts + 1):
            response = self.client.chat.completions.create(
                model=model,
                messages=history,
                temperature=temperature,
                response_format=response_format,
            )
            usage = response.usage
            result["usage"]["completion_tokens"] += usage.completion_tokens
            result["usage"]["prompt_tokens"] += usage.prompt_tokens
            result["usage"]["total_tokens"] += usage.total_tokens
            print(
                f"attempt={attempt} prompt={usage.prompt_tokens} "
                f"completion={usage.completion_tokens} total={usage.total_tokens}"
            )

            raw = response.choices[0].message.content
            try:
                data = json.loads(raw)
                if schema is not None:
                    result["content"] = schema.model_validate(data)
                else:
                    result["content"] = data
                result["success"] = True
                result["error"] = None
                return result
            except (json.JSONDecodeError, ValidationError) as e:
                last_error = e
                print(f"attempt={attempt} schema 失败: {e}")
                history.append({"role": "assistant", "content": raw})
                history.append(
                    {
                        "role": "user",
                        "content": f"按 schema 修正 json，错误：{e}",
                    }
                )

        result["error"] = last_error
        return result
