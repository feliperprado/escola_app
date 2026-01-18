# Configuração da Aplicação Flask

import os
from datetime import timedelta

class Config:
    """Configurações base para a aplicação"""
    
    # Flask
    DEBUG = False
    TESTING = False
    
    # Sessão
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # True em produção com HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Segurança
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Google Sheets
    CREDENTIALS_FILE = 'credentials.json'
    SPREADSHEET_NAME = 'Sistema_Frequencia_Escola'
    
    # Uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = 'uploads'

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    # Em produção, defina uma SECRET_KEY forte
    SECRET_KEY = os.environ.get('SECRET_KEY', 'CHANGE-THIS-SECRET-KEY-IN-PRODUCTION')

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    DEBUG = True

# Selecionar configuração baseada na variável de ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Retorna a configuração apropriada"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
