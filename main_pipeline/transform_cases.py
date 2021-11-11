import pandas as pd
from extract import save_to_csv_temp
import transform
import validate
import logging
import os

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
    )
logger = logging.getLogger(__name__)

# Set the path to the temp folder
path = os.path.join(os.path.dirname(__file__), 'temp', 'cleaned_cases.csv')

# Define the new column names
cols = [
        'area_code',
        'area_name',
        'area_type',
        'date',
        'new_cases',
        'nation',
        'id'
        ]

# Read the raw data
def read_csv_temp(file_name: str) -> pd.DataFrame:
    """
    Reads the csv file from the temp folder
    """
    return pd.read_csv(file_name)

# Run the transformation
def main():
    logger.info("Reading Raw Cases data")
    df = read_csv_temp(os.path.join(os.path.join(os.path.dirname(__file__)), 'temp', 'cases.csv'))
    logger.info("Reading raw cases data Completed")
    logger.info("Transforming raw cases data")
    df = transform.parse_dates(df, ['date'])
    df = transform.create_country_col(df)
    df = transform.create_unique_from_columns(df)
    df.columns = cols
    logger.info("Transformation Completed (raw cases)")
    logger.info("Validating data")
    tests = validate.data_validation_tests
    if not validate.validate_data(df, tests):
        raise Exception('Data validation failed, terminating ETL.')
    save_to_csv_temp(df, path)
    logger.info("Saving transformed Cases Completed")

if __name__ == '__main__':
    main()
    