# import os

# class Config:
#   DEBUG = False
#   SECRET_KEY = os.environ.get('SECRET_KEY') or 'ALWAYS_CAREFUL_AND_NEVER_AFRAID'
#   DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgresql://postgres:root@http://3.209.126.143/diarydawndb'
#   REDIS_HOST = os.environ.get('REDIS_HOST') or 'http://' + os.getenv('REDIS_HOST', 'localhost') + ':6379'
#   REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
#   REDIS_DB = os.environ.get('REDIS_DB') or 0
#   # Add other production-specific configurations here