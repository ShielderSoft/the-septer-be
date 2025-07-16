from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str
    jwt_secret: str
    gemini_api_base: str
    max_file_size_mb: int = 10

    # AES encryption secrets (must be set in .env)
    septer_aes_secret: str
    septer_aes_salt: str
    septer_aes_iv_base: str

    class Config:
        env_file = ".env"
        extra = "forbid"  # default in Pydantic v2 — ensures no unknown env vars

settings = Settings()
