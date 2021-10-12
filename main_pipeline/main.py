import logging
import sys
import os
from dotenv import load_dotenv

import extract
import transform
import validate
import load

# Set up logging
logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


# Load credentials from .env file, if needed
if not os.getenv('PG_CONN_CRED'):
    load_dotenv()
PG_CONN_CRED = os.getenv('PG_CONN_CRED')

def main(src, dest, options):
    """
    """
    logger.info("Starting ETL")

    #Extract
    logger.info(f"Extracting {options[options.index('-name') + 1]} data...")
    df = extract.get_csv_from_requests(src)

    # Transformation
    logger.info(f"Transforming {options[options.index('-name') + 1]} data....")
    optional_args =[opt[1:] for opt in options if opt.startswith("-")]
    if "transform" in optional_args:

        df = transform.parse_dates(df, ['date'])
        df = transform.create_country_col(df)
        if {options[options.index('-name') + 1].lower()} == "cases":
            df.columns = [
                'area_code',
                'area_name',
                'area_type',
                'date',
                'new_cases',
                'nation'
                ]
            logger.info(f"{df.columns}")
        elif {options[options.index('-name') + 1].lower()} == "deaths":
             df.columns = [
                'area_code',
                'area_name',
                'area_type',
                'date',
                'new_death',
                'nation'
                ]
        elif  {options[options.index('-name') + 1].lower()} == "vaccinations":
             df.columns = [
                'area_code',
                'area_name',
                'area_type',
                'date',
                'vaccinations',
                'nation'
                ]
    else:
        logger.info("No transformation specified")          
    logger.info("Transformation complete")


    # Validation
    logger.info(f"Validating {options[options.index('-name') + 1]} data...")
    if "validate" in optional_args:
        tests = validate.data_validation_tests
        if not validate.validate_data(df, tests):
            raise Exception('Data validation failed, terminating ETL.')
        
    else:
        logger.info("No Validation specified. Skipping Validation")

    # Loading
    logger.info(f"Loading {options[options.index('-name') + 1]} to database...")
    load.load_to_table(df, dest, PG_CONN_CRED)
    logger.info("Loading complete...")




if __name__ == "__main__":

    logger.info('Parsing command...')
    options = sys.argv[1:]

    src, dest = options[-2:]

    opt_args = options[:-2]

    logger.info("Starting ETL...")
    main(src, dest, opt_args)