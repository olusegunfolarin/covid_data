import logging
import pandas as pd
from datetime import date


logger = logging.getLogger(__name__)


def unique_records(df):
    """
    Checks that data contains unique records
    """
    return df[[df.columns[0], 'date']].duplicated().sum() == 0

def valid_date(df):
    """
    Validate date is not in the future
    """
    today = date.strftime(date.today(), format="%Y-%m-%d")
    return (df['date'] <= today).sum() == len(df)

def cases_range(df, col=4, min=0, max=1e7):
    """Validates cases are not negative or more than the population of UK
    """
    col = df.columns[4]
    return (df[col] >= min).all() & (df[col] <=max).all()

def no_nulls(df):
    """Validates that data contains no null values
    """
    return df.isnull().values.sum() == 0

# validation for cases data
data_validation_tests = [
    (unique_records, "Only one record per local authority per date allowed"),
    (valid_date, "Date cannot be in the future"),
    (cases_range, "Cases can only be between 0 and 66 million"),
    (no_nulls, "Data cannot contain null values")
]


def validate_data(df, tests):
    """Run tests on data for data validation

    Parameters
    ---------
    df: DataFrame object
        Dataset to test
    tests: dict
        A mapping of test function to failure messages

    Returns
    -------
    bool
    """
    results = []
    for test, message in tests:
        results.append(test(df.copy()))
        if results[-1]:
            logger.info(f"Data validation {test.__name__} passed.")
        else:
            logger.error(f"Data validation {test.__name__} failed. {message}")
    logger.info(f"{sum(results)/len(results)} passed.")
    return sum(results) == len(results)



if __name__ == "__main__":
    df = pd.read_csv("/home/olusegun/projects/covid_data/dev.csv")
    print(cases_range(df))