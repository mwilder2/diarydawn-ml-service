from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import os
from dotenv import load_dotenv
load_dotenv()
db = SQLAlchemy()

# Initialize Redis client
# redis_client = Redis(
#     host=os.getenv('REDIS_HOST', 'localhost'),
#     port=int(os.getenv('REDIS_PORT', 6379)),
#     db=int(os.getenv('REDIS_DB', 0))
# )

# Initialize Redis client
# Assuming Redis configurations are stored in the Flask app config
# redis_client = Redis()

def create_redis_client(app=None):
    # This always returns a Redis object, regardless of whether app is provided
    return Redis(
        host=os.getenv('REDIS_HOST', 'redis'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        # db=int(os.getenv('REDIS_DB', 0))
    )

redis_client = create_redis_client()