## Flask ML Service
This is the Flask-based service for Diary Dawn, responsible for processing diaries using machine learning models. It interacts with the Nest.js backend via Redis, retrieves diary entries, applies machine learning models for analysis, and updates the results back into the database.

## Features
Processes diary entries using machine learning models.
Communicates with the main backend (Nest.js) via Redis for seamless integration.
Saves results in the database after processing.
Serves the ML models through a production-ready Gunicorn setup.
Requirements
Python 3.9+
Redis (for Pub/Sub communication with the Nest.js backend)
Docker (optional, for containerized deployment)

Installation
1. Clone the Repository


git clone https://github.com/your-username/diarydawn-ml-service.git
cd diarydawn-ml-service
2. Install Dependencies
Using pip:

pip install -r requirements.txt

3. Database Migration
While migrations are handled by the Nest.js backend, the Flask service supports migration commands for local development:

flask db init       # Initializes migrations (run only once)
flask db migrate    # Generates migration scripts
flask db upgrade    # Applies the migrations
Running the Service
Local Development
To start the Flask application locally:

flask run
The app will run on http://127.0.0.1:5000 by default.

Production Deployment
The service uses Gunicorn for production. You can start the app with the following command:

gunicorn -w 4 app.main:app --bind 0.0.0.0:8000 --log-level=debug
Alternatively, use Docker for a containerized deployment.

Using Docker
Build and run the Docker container:

docker build -t diarydawn-ml-service .
docker run -p 8000:8000 diarydawn-ml-service
Directory Structure
.
├── app/                # Flask application code
├── migrations/         # Database migrations (if used)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Production Docker setup
├── README.md           # This file
└── ...

Communication with Backend
The service uses Redis for communication with the Nest.js backend. Ensure Redis is running and properly configured in both services.

## General Notes
Models and Data: Ensure all ML models, tokenizers, and related files are present in the correct directory as referenced by the application.
Environment Variables: Configure any sensitive information like database URLs or Redis connections via .env files or environment variables.
This README should serve as a comprehensive overview of your Flask ML service. If there's anything specific you'd like to add or emphasize, let me know!


## Notes on Pretrained Models
The Flask ML service relies on DistilBERT pretrained models for its machine learning functionality. These models are essential for processing diary entries but are too large to upload to the repository due to their size (250 MB to 500 GB each, with 16 models in total).

To handle this:
1. Model Storage: The pretrained models are stored externally on flash drives.
2. Loading Models: Before starting the Flask service, ensure the models are accessible by either:
Plugging in the flash drives and configuring the paths in the application settings.
Hosting the models on a local server or cloud storage with accessible download links.
3. Configuring Paths: Update the model paths to point to the directory where the models are stored.

## Handling Large Models
If you're replicating this project:
1. For Local Development: Copy the models from the flash drives to your local system and update the paths in the Flask application settings.

2. For Production: Consider using cloud storage services like AWS S3, Google Cloud Storage, or Azure Blob Storage to store and serve the models. Use pre-signed URLs or direct links for efficient access.
Example Configuration
Add a .env file or update your environment variables with:

SQLALCHEMY_DATABASE_URI=postgres-database
SECRET_KEY=secrete-key
REDIS_HOST=redis-host
REDIS_PORT=redis-port
REDIS_DB=redis-db

## Deployment Constraints
Due to the model sizes:
The repository does not include the pretrained models.
Ensure the Flask service has access to the models before deployment.
Use efficient model loading and caching mechanisms to minimize runtime overhead.
