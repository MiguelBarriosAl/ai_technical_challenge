from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings managed via Pydantic.
    Loads configuration from environment variables and a .env file.
    """

    LITELLM_API_KEY: str | None = None
    QDRANT_URL: str = "http://localhost:6333"
    ENVIRONMENT: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
