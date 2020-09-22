"""Flask config."""
from os import environ
from tempfile import mkdtemp
from dotenv import load_dotenv

# Load enviroment variables from .env file in current directory
load_dotenv()

# Get secret key from environment variable
SECRET_KEY = environ.get('SECRET_KEY')

# Ensure templates are auto-reloaded
TEMPLATES_AUTO_RELOAD = True

# Configure session to use filesystem (instead of signed cookies)
SESSION_FILE_DIR = mkdtemp()
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
