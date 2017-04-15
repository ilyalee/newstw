import os
from os.path import join, dirname
from dotenv import load_dotenv
from utils.type_utils import sint
import sys

filename = ".env"
dotenv_path = join(dirname(__file__), filename)

load_dotenv(dotenv_path)
TESTING = os.environ.get("TESTING")

# Local database url
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_TESTING_URL = os.environ.get("DATABASE_TESTING_URL")

# Facebook Graph API
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_API_VERSION = os.environ.get("FACEBOOK_API_VERSION")

# salt for Hashids
SALT = os.environ.get("SALT")

# time zone
TIMEZONE = os.environ.get("TIMEZONE")

LIMIT = sint(os.environ.get("LIMIT"), 1)

CONNECTIONS_PER_FEED = sint(os.environ.get("CONNECTIONS_PER_FEED"), 100)

DELETE_KEY = os.environ.get("DELETE_KEY")
