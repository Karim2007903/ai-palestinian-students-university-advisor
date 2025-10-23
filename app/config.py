from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Palestinian Student Academic Guidance Agent"
    environment: str = "development"
    dataset_path: str = "/workspace/app/data"
    default_top_k: int = 10


settings = Settings()
