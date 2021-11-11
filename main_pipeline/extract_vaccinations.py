from extract import get_csv_from_requests, save_to_csv_temp
import logging
import os
import sys

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
    )
logger = logging.getLogger(__name__)

# # Set the url to extract data from
# url = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newPeopleVaccinatedCompleteByVaccinationDate&format=csv'
    
# Set the path to save the data to
path = os.path.join(os.path.dirname(__file__), 'temp', 'vaccinations.csv')
    
# Extract the data
def main():
    logger.info('Starting Vaccinations Extraction')
    csv_data = get_csv_from_requests(url)
    logger.info('Finished Extracting Vaccinations')
    logger.info('Staging extracted data')
    save_to_csv_temp(csv_data, path)
    logger.info('Staging complete for Vaccinations')
    
# Run the main function
if __name__ == '__main__':
    # Set the url to the data source from the command line
    url = sys.argv[1]
    main()