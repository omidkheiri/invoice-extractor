from pathlib import Path
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

base_dir = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    openai_api_key: SecretStr = Field(..., description="OpenAI API key for accessing the OpenAI services.")
    llm_model: str = Field(default="gpt-4o", description="The language model to be used for generating responses.")
    max_retries: int = Field(default=3, ge=1, le=5, description="Maximum number of retries for API requests.")
    temperature: float = Field(default=0.0, description="Sampling temperature for response generation.")

    raw_data_dir: Path = Field(default=base_dir / "data" / "raw", description="Directory path for storing raw data.")
    processed_data_dir: Path = Field(default=base_dir / "data" / "processed", description="Directory path for storing processed data.")

    model_config = SettingsConfigDict(env_file=base_dir / ".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()