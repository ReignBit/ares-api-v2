"""
    HOW TO USE:
        -   Create a new file (config.py)
        -   Import from here either TestingConfig, ProductionConfig, or DevelopmentConfig
        -   Edit settings (SQLALCHEMY_DATABASE_URI, SQLALCHEMY_BINDS, TESTING, DEBUG, ect..)
        -   When calling create_app() pass in the
            import path to your new config (app.config.ConfigNameHere)
"""

from werkzeug.security import generate_password_hash


class Config:
    """Base class for all Config objects"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_BINDS = {
        "kat_backend": "Your uri here",
        "supervisor_backend": "Your uri here"
    }


class DevelopmentConfig(Config):
    """Development config - Used for development environments"""
    # Subclass this and change settings to your desire
    DEBUG = True
    AUTH_USERS = {"USERNAME": generate_password_hash("PASSWORD")}


class TestingConfig(Config):
    DEBUG = False
    TESTING = True

    AUTH_USERS = {"test": generate_password_hash("test")}

    # Create database in memory instead of on disk/network for testing
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_BINDS = {
        "kat_backend": "sqlite://",
        "supervisor_backend": "sqlite://",
    }



class ProductionConfig(Config):
    """Production config - Used for production environments"""
    # Subclass this and change settings to your desire
    AUTH_USERS = {"USERNAME": generate_password_hash("PASSWORD")}
