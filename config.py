import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jala-academy-secret-key-2024'

    # Use Render's PostgreSQL database
    raw_db_url = os.environ.get('DATABASE_URL')

    # Fix: Convert 'postgres://' → 'postgresql://'
    if raw_db_url and raw_db_url.startswith('postgres://'):
        raw_db_url = raw_db_url.replace('postgres://', 'postgresql://', 1)

        # Never fall back to SQLite
    if not raw_db_url:
        raise ValueError("DATABASE_URL is not set. Cannot connect to database.")

    SQLALCHEMY_DATABASE_URI = raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)