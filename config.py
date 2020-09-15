"""Flask config."""
from os import environ
from dotenv import load_dotenv

# Load enviroment variables from .env file in current directory
load_dotenv()

# Get secret key from environment variable
SECRET_KEY = environ.get('SECRET_KEY')
