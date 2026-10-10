import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "prod-secure-student-erp-secret-key-2026-x99")
    
    # Dual database support: MySQL when configured, otherwise SQLite fallback
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(BASE_DIR, 'student_erp.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload Configurations
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024  # 30 MB max
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "ppt", "pptx", "txt", "png", "jpg", "jpeg"}
    
    # Institution Profile
    INSTITUTION_NAME = os.environ.get("INSTITUTION_NAME", "Apex Institute of Higher Education & Technology")
    INSTITUTION_CODE = os.environ.get("INSTITUTION_CODE", "AIHET-2026")
    INSTITUTION_TAGLINE = "Excellence in Academic Management & Research"
    
    # Attendance Policy
    MINIMUM_ATTENDANCE_PERCENTAGE = 75.0
    
    # Session Security
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
