import time
import openai
from pathlib import Path
from .config import settings

openai.api_key = settings.get('api_key', '')


def call_openai(prompt: str, content: str) -> str:
    if not openai.api_key or openai.api_key == 'YOUR_OPENAI_API_KEY':
        return f"Mock response for: {prompt[:10]}"
    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model=settings.get('model', 'gpt-4'),
                messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}],
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error: {e}, retrying...")
            time.sleep(2 ** attempt)
    raise RuntimeError('Failed after retries')


def stage_a(prompt: str, transcript: str) -> str:
    result = call_openai(prompt, transcript)
    print("=== END STAGE A ===")
    return result


def stage_b(prompt: str, transcript: str) -> str:
    result = call_openai(prompt, transcript)
    print("=== END STAGE B ===")
    return result


def stage_c(prompt: str, stage_a_result: str, stage_b_result: str) -> str:
    combined = stage_a_result + "\n" + stage_b_result
    result = call_openai(prompt, combined)
    print("=== END STAGE C ===")
    return result
