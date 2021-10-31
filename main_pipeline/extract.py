import pandas as pd
import requests 
import logging
import io


logger = logging.getLogger(__name__)

def get_csv_from_requests(url):
    """
    Extracts data from web using a GET requests

    Parameters
    ----------
    url: str
        URL for the extraction endpoint.

    Returns
    -------
    Dataframe
    """
    r = requests.get(url, timeout=30)
    data = r.content.decode("utf-8")
    df = pd.read_csv(io.StringIO(data), low_memory=False)
    return df



def save_to_csv_temp(df, path):
    """Saves the extracted data to CSV to be used later

    Parameters
    ----------
    df: dataframe
        The dataframe to save to csv
    path: str
        Path to which the csv is saved
    
    Returns:
    --------
    A file saved to temporary location on machine

    """

    df.to_csv(path, index=False)



if __name__ == "__main__":
    df = get_csv_from_requests("https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newDeaths28DaysByDeathDate&format=csv")
    print(df.head())