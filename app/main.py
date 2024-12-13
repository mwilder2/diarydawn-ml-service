import json
import logging
import os
from threading import Thread
from flask import Config, Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.extensions import db, redis_client
from redis import Redis
from sqlalchemy.orm import joinedload
from app.ml.ml_command import process_ml_for_book, process_text_for_public
from app.pub_sub.publisher import publish_complete_message, publish_response_to_nest
from flask_migrate import Migrate
from app.common.database.models.user import User
from app.common.database.models.book import Book
from app.common.database.models.profile import Profile
from app.common.database.models.result import Result
from app.common.database.models.page import Page
from app.common.database.models.limitless import Limitless
from app.common.database.models.gratitude import Gratitude
from app.common.database.models.affirmation import Affirmation
from app.common.database.models.lesson import Lesson
from app.common.database.models.journey import Journey
from app.common.database.models.emotion import Emotion
from app.common.database.models.dream import Dream
from app.common.logger.custom_logger import setup_logger


# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

CORS(app)


db.init_app(app)

migrate = Migrate(app, db)

logger = setup_logger()

def start_listener_thread(app):
    with app.app_context():
        try:
            listener_thread = Thread(target=listen_for_messages, daemon=True)
            listener_thread.start()
        except Exception as e:
            logging.error(f"Failed to start the listener thread: {e}")

def listen_for_messages():
    try:
        pubsub = redis_client.pubsub()
        pubsub.subscribe(['generate-strengths-channel'])
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'].decode('utf-8'))
                
                print(f"Received message: {data}")
                if 'userId' in data and 'bookId' in data:
                    user_id = data['userId']
                    book_id = data['bookId']
                    
                    with app.app_context():
                       process_ml_for_book(user_id, book_id)
                elif 'text' in data:
                    # Handle text for non-registered user
                    text = data['text']
                    with app.app_context():
                       process_text_for_public(text)
                else:
                    # Message format not recognized
                    error_response = {
                        'error': 'Unexpected message format',
                        'detail': 'The message did not contain the expected keys.'
                    }
                    publish_response_to_nest('flask-nest-error-channel', error_response)

    except Exception as e:
        logging.error(f"Error listening for messages: {e}")
        
def post_fork(server, worker):
    start_listener_thread(app)
    logger.info("Worker started")
def child_exit(server, worker):
    server.log.info("Worker %s exiting.", worker.pid)
    
    
post_fork(app, None)
# child_exit(app, None)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    logger.info('Starting the Flask application...')
    app.run(host='0.0.0.0', port=8000)
    
# Steps for migration

# Step 1:
# flask db init app.main:app

# Step 2:
# flask db migrate

# Step 3:
# flask db upgrade

# flask db init        # Initializes a migration directory (only done once)
# flask db migrate     # Generates a migration script from model changes
# flask db upgrade     # Applies the migration to the database
# flask db downgrade   # Reverts the last migration
# flask db history     # Shows the history of migrations