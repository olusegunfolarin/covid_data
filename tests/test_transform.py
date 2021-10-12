import pytest
import pandas as pd
from main_pipeline import transform


@pytest.fixture(scope='module')
def df():
    df = pd.read_csv("/home/olusegun/projects/covid_data/dev.csv")
    return df


def test_date_parse(df):
    df = transform.parse_dates(df, ['date'])
    assert df['date'].dtype == 'datetime64[ns]'


def test_country_column(df):
    df = transform.create_country_col(df)
    assert 'nation' in df.columns

