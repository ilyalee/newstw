import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Local database url
DATABASE_URL = os.environ.get("DATABASE_URL")

# Facebook Graph API
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_API_VERSION = os.environ.get("FACEBOOK_API_VERSION")
