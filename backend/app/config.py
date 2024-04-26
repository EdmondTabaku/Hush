import os


class Config:
    # Frontend configuration
    FRONTEND_URL = os.environ.get('FRONTEND_URL') or 'http://localhost:3000'
