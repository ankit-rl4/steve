# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure configuration
subscription_id = os.getenv('SUBSCRIPTION_ID')
resource_group = os.getenv('RESOURCE_GROUP')
workspace_name = os.getenv('WORKSPACE_NAME')
