# Load environment variables from .env file
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    # Correctly assign environment variables to broker and backend variables
    broker = os.getenv('CELERY_BROKER_URL')  # Remove the comma at the end of this line
    backend = os.getenv('CELERY_RESULT_BACKEND')
