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

    # SQLAlchemy configuration – uses MySQL via PyMySQL driver.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://clouduser:StrongPassword123@localhost:3306/clouddrive"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS S3 Configurations
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
