import instructor
from openai import OpenAI
from src.config import settings


def get_instructor_client() -> instructor.Instructor:
    raw_client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
    return instructor.from_openai(raw_client)