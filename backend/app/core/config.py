"""应用配置"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # 应用
    APP_NAME: str = "算法研发管理平台"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # JWT
    SECRET_KEY: str = "algo-platform-secret-key-please-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # 数据库（SQLite）
    DB_PATH: str = str(Path(__file__).resolve().parent.parent.parent / "data" / "app.db")

    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite:///{self.DB_PATH}"

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]


settings = Settings()
