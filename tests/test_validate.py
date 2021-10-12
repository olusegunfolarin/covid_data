import pytest
import pandas as pd
from main_pipeline import validate


@pytest.fixture(scope='module')
def df():
    df = pd.read_csv("/home/olusegun/projects/covid_data/dev.csv")
    return df

@pytest.fixture()
def cases():
    return  [
    (validate.unique_records, "Only one record per local authority per date allowed"),
    (validate.valid_date, "Date cannot be in the future"),
    (validate.cases_range, "Cases can only be between 0 and 66 million"),
    (validate.no_nulls, "Data cannot contain null values")
    ]
def test_unique_records(df):
    assert validate.unique_records(df) == True

def test_no_nulls(df):
    assert validate.no_nulls(df) == True

def test_valid_dates(df):
    assert validate.valid_date(df) == True

def test_cases_range(df):
    assert validate.cases_range(df) == True
    assert validate.cases_range(df, min=100, max = 1000) == False

def test_data_validation(df, cases):
    assert validate.validate_data(df, cases) == True