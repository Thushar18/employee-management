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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/employee_management'


    if 'postgres://' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://')
    
    # Disable SQLAlchemy event system (to save resources)
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