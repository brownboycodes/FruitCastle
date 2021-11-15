"""Flask configuration."""

class Config:
    """Base config."""
    SECRET_KEY = "123"
    STATIC_URL_PATH="/dist"
    STATIC_FOLDER = 'dist'
    TEMPLATE_FOLDER = 'client'


class DevConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    TESTING = False
