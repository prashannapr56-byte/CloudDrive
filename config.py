import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
if env_path.is_file():
    load_dotenv(dotenv_path=env_path)

class Config:
    """Application configuration settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change')

    # SQLAlchemy configuration – fallbacks to SQLite if no cloud database URL is provided.
    # Automatically handles 'postgres://' schema mapping to 'postgresql://' for Render/Heroku compatibility.
    _raw_db_url = os.getenv("DATABASE_URL")
    if _raw_db_url and _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)
    
    if _raw_db_url:
        SQLALCHEMY_DATABASE_URI = _raw_db_url
    elif os.getenv("VERCEL"):
        # Vercel serverless functions have a read-only filesystem except for the /tmp folder
        SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/clouddrive.db"
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///clouddrive.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS S3 Configurations - supports S3_ prefixed fallbacks to bypass Vercel reserved keyword restrictions
    AWS_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("S3_REGION") or os.getenv("AWS_REGION", "us-east-1")
    AWS_S3_BUCKET = os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET")
