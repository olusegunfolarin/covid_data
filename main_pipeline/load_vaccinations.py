import pandas as pd
import load
import logging
import os
import sys
from dotenv import load_dotenv

# setting up logging
logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Load credentials from .env file, if needed
if not os.getenv('PG_CONN_CRED'):
    load_dotenv()
PG_CONN_CRED = os.getenv('PG_CONN_CRED')


# Read the cleaned data
def read_csv_temp(file_name: str) -> pd.DataFrame:
    """
    Reads the csv file from the temp folder
    """
    return pd.read_csv(file_name)



# Define function to load vaccinations data
def main(dest):
    logger.info('Loading transformed vaccination data')
    df = read_csv_temp(os.path.join(os.path.join(os.path.dirname(__file__)), 'temp', 'cleaned_vaccinations.csv'))
    logger.info('Loading vaccinations data to data warehouse')
    load.load_to_table(df, dest, PG_CONN_CRED)
    logger.info("Loading complete")
    


if __name__ == '__main__':
    # Get command line arguments
    dest = sys.argv[1]
    main(dest)