"""
Configuration file for Fee Management System

This file contains all configuration settings for the application.
We use environment variables for sensitive data and defaults for development.
"""

import os
from datetime import timedelta

# Get the base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class
    
    This contains default settings that work for development.
    We can create other classes (like ProductionConfig) that inherit from this.
    """
    
    # ========== SECRET KEY ==========
    # Flask needs a secret key for sessions and CSRF protection
    # In production, this should be set via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # ========== DATABASE CONFIGURATION ==========
    # SQLite database path
    # We store it in the 'instance' folder (Flask convention)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'fms.db')
    
    # Disable SQLAlchemy event system (saves resources)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ========== SESSION CONFIGURATION ==========
    # Session timeout: 30 minutes of inactivity
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Session cookie settings
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access (security)
    SESSION_COOKIE_SECURE = False   # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    
    # ========== INTERNATIONALIZATION (i18n) ==========
    # Supported languages
    LANGUAGES = {
        'ur': 'Urdu',
        'en': 'English'
    }
    
    # Default language (Urdu)
    BABEL_DEFAULT_LOCALE = 'ur'
    
    # Default timezone
    BABEL_DEFAULT_TIMEZONE = 'Asia/Karachi'
    
    # ========== FILE UPLOADS ==========
    # Maximum file size: 16MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Upload folder for student photos, receipts, etc.
    UPLOAD_FOLDER = os.path.join(basedir, 'media')
    
    # ========== LOGGING ==========
    # Log file path
    LOG_DIR = os.path.join(basedir, 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'fms.log')
    
    # Log file max size: 10MB
    LOG_FILE_MAX_SIZE = 10 * 1024 * 1024
    
    # Number of backup log files to keep
    LOG_BACKUP_COUNT = 5
    
    # ========== BACKUP ==========
    # Backup directory
    BACKUP_DIR = os.path.join(basedir, 'backups')
    
    # ========== PAGINATION ==========
    # Records per page
    RECORDS_PER_PAGE = 50
    
    # ========== RECEIPT SETTINGS ==========
    # Receipt number format
    RECEIPT_NUMBER_PREFIX = 'RCP'
    GROUP_RECEIPT_NUMBER_PREFIX = 'GP'
    
    # Student ID format
    STUDENT_ID_PREFIX = 'SCH'
    FAMILY_ID_PREFIX = 'FAM'


class DevelopmentConfig(Config):
    """
    Development configuration
    
    Used when running the app in development mode.
    Enables debugging and detailed error messages.
    """
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """
    Production configuration
    
    Used when running the app in production.
    Disables debugging and uses secure settings.
    """
    DEBUG = False
    TESTING = False
    
    # In production, use environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_SECURE = True  # Requires HTTPS


class TestingConfig(Config):
    """
    Testing configuration
    
    Used when running tests.
    Uses a separate test database.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests


# Configuration dictionary
# Maps environment names to config classes
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
