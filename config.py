import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tracksy-super-secret-key-12345')
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tracksy.db')
