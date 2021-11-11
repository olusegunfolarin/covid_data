import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine


# Load credentials from .env file, if needed
if not os.getenv('PG_CONN_STRING'):
    load_dotenv()
PG_CONN_STRING = os.getenv('PG_CONN_STRING')
###############################################################################
# need to come back to this.
# need to come back to this.