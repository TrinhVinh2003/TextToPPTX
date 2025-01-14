import enum
from pathlib import Path
from tempfile import gettempdir
from pydantic_settings import BaseSettings, SettingsConfigDict

TEMP_DIR = Path(gettempdir())

class LogLevel(str, enum.Enum):
    """Possible log levels."""
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

class Settings(BaseSettings):
    """
    Application and project settings loaded from environment variables.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Application settings
    APP_TITLE: str = "Text to Powerpoint"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Text to Powerpoint is a service that converts text to PowerPoint slides."
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # Database settings
    APP_DB_HOST: str = "app-db"
    APP_DB_HOST_NAME: str = "app-db"
    APP_DB_PORT: int = 5432
    APP_DB_USER: str = "app"
    APP_DB_PASS: str = "app"
    APP_DB_BASE: str = "app"

    # Media directory
    APP_MEDIA_DIR: Path = Path("app/static/media")

    # Project-specific settings
    PROJECT_NAME: str = "Text to Powerpoint"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "Text to Powerpoint is a service that converts text to PowerPoint slides."
    DEBUG: bool = True
    OPENAI_BASE_URL: str 
    OPENAI_API_KEY: str
    REDIS_ENABLE: bool = True
    REDIS_URL: str = "redis://localhost:6379/0"
    HOST_URL: str = "http://localhost:5000"
   

    # Logging
    log_level: LogLevel = LogLevel.INFO

    # Pexel API
    PEXELS_API: str

    # Host Server
    host_server: str 

    # Directories
    pdf_dir: Path = Path("E:/web/TexttoPPtx/fastapi-dify-tool-template/app/web/static/upload")
    media_dir: Path = Path("E:/web/TexttoPPtx/fastapi-dify-tool-template/app/web/static/media")

    @property
    def media_dir_static(self) -> Path:
        """Get path to the media directory."""
        self.media_dir.mkdir(parents=True, exist_ok=True)
        return self.media_dir

    @property
    def media_base_url(self) -> str:
        """Get base URL for media files."""
        if self.domain:
            return f"{self.domain}/static/media"
        return f"http://{self.host}:{self.port}/static/media"

    @property
    def is_debug_mode(self) -> bool:
        """Check if the application is in debug mode."""
        return self.APP_DEBUG or self.DEBUG

settings = Settings()