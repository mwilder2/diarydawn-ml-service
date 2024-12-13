# publisher.py
import json
import logging
from app.extensions import redis_client

def publish_complete_message(user_id: int, book_id: int):
    try:
        message = {'userId': user_id, 'bookId': book_id}
        redis_client.publish('flask-completion-channel', json.dumps(message))
        # Optionally, return True for success or log the event
    except Exception as e:
        logging.error(f"Error publishing message: {e}")
        
def publish_response_to_nest(channel, message):
    try:
        # message could be a dictionary containing various types of responses
        # Ensure it's JSON-serialized before publishing
        serialized_message = json.dumps(message)
        redis_client.publish(channel, serialized_message)
        # Optionally, log the successful publication of the message
    except Exception as e:
        logging.error(f"Error publishing response message to Nest.js: {e}")
        
def publish_public_results_complete_message(results):
    try:
        # Convert results dictionary into a list of its values
        results_list = list(results.values())
        redis_client.publish('public-strengths-completion-channel', json.dumps(results_list))
    except Exception as e:
        logging.error(f"Error publishing message: {e}")


