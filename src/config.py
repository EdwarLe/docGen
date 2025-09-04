class Config:
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    
config = {
    'development': DevelopmentConfig
}
    