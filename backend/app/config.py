import os


class Config:
    # Secret key for sessions and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

    # Frontend configuration
    FRONTEND_URL = os.environ.get('FRONTEND_URL') or 'http://localhost:3000'
