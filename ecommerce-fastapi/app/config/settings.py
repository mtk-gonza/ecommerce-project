from typing import List, ClassVar, Optional
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # =========================
    # 🔹 ENTORNO
    # =========================
    ENVIRONMENT: str = "dev"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    # =========================
    # 🔹 BASE DIR (NO es env)
    # =========================
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent

    # =========================
    # 🔹 CONFIG GENERAL
    # =========================
    API_URL: str = "http://localhost:3050"
    API_PORT: int = 3050
    WEB_PORT: int = 3060
    API_V1_PREFIX: str = "/api/v1"

    SECRET_KEY: str = "ThisIsNotSecret"
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ACCESS_TOKEN_EXPIRE_HOURS: int = 2

    # =========================
    # 📁 PATHS (NO env)
    # =========================
    UPLOADS_DIR: ClassVar[Path] = BASE_DIR / "uploads"
    IMAGES_DIR: ClassVar[Path] = UPLOADS_DIR / "images"

    # =========================
    # 🔹 DATABASE
    # =========================
    DB_TYPE: str = "sqlite"

    SQLITE_DB: str = "ecommerce-dev.db"

    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int = 3306
    DB_NAME: str | None = None

    # =========================
    # 🔹 CORS
    # =========================
    CORS_ALLOW_ORIGINS: str = "*"

    # ==================== MERCADOPAGO ====================
    MERCADOPAGO_ACCESS_TOKEN: str
    MERCADOPAGO_PUBLIC_KEY: str
    MERCADOPAGO_SANDBOX: bool
    
    # URLs para redirección después del pago
    PAYMENT_SUCCESS_URL: str = f"{API_URL}/payment/success"
    PAYMENT_PENDING_URL: str = f"{API_URL}/payment/pending"
    PAYMENT_FAILURE_URL: str = f"{API_URL}/payment/failure"
    
    # Webhook
    PAYMENT_WEBHOOK_URL: str = "https://tudominio.com/api/v1/payments/webhook"
    PAYMENT_WEBHOOK_SECRET: Optional[str]
    
    # Timeouts y reintentos
    PAYMENT_TIMEOUT_SECONDS: int = 30
    PAYMENT_MAX_ATTEMPTS: int = 3

    # =========================
    # ⚙️ PYDANTIC CONFIG
    # =========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # 🔥 importante
        case_sensitive = True
    )

    # =========================
    # 🌐 CORS
    # =========================
    @property
    def cors_origins_list(self) -> List[str]:
        if self.CORS_ALLOW_ORIGINS == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ALLOW_ORIGINS.split(",")]

    # =========================
    # 🗄️ DATABASE URL
    # =========================
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "sqlite":
            return f"sqlite:///./{self.SQLITE_DB}"

        if not all([self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME]):
            raise ValueError("Faltan variables para MySQL")

        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # =========================
    # 🔹 HELPERS
    # =========================
    @property
    def is_dev(self) -> bool:
        return self.ENVIRONMENT == "dev"


settings = Settings()