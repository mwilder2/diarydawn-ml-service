import logging
from flask import Flask
from logging.handlers import RotatingFileHandler


def setup_logger():
    # Create a logger object
    logger = logging.getLogger('MyFlaskAppLogger')
    logger.setLevel(logging.INFO)  # You can set this to DEBUG, INFO, WARNING, ERROR

    # Create a file handler that logs messages to a file
    handler = RotatingFileHandler('flask_app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    return logger

# Setup the logger
# logger = setup_logger()