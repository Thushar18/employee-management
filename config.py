import os
from datetime import timedelta

class Config:
    """
    Configuration class for the Flask application.
    Uses environment variables if available; otherwise, falls back to defaults.
    """
    # Secret key for session management and security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jala-academy-secret-key-2024'

    # Database configuration
    # Uses DATABASE_URL from environment, or defaults to MySQL with PyMySQL
    # Use PostgreSQL on Render
    # Get DATABASE_URL from environment (set by Render)
    raw_db_url = os.environ.get('DATABASE_URL')
    
    # Fix for Render: they use 'postgres://' but SQLAlchemy needs 'postgresql://'
    if raw_db_url and raw_db_url.startswith('postgres://'):
        raw_db_url = raw_db_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = raw_db_url or 'postgresql://localhost/employee_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail settings for password reset functionality
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Should be set in environment
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Use App Password for Gmail

    # File upload settings
    UPLOAD_FOLDER = 'static/uploads'  # Directory to store uploaded employee images
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size (to prevent large uploads)

    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)  # Session expires after 1 hour