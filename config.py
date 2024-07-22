# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure configuration
ENDPOINT = os.getenv('API_ENDPOINT')
KEYAPI = os.getenv('API_KEY')
