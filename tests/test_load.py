import pytest
import pandas as pd
from main_pipeline import load, transform
import dotenv
import os
from sqlalchemy import create_engine


@pytest.fixture(scope='module')
def df():
    df = pd.read_csv("/home/olusegun/projects/covid_data/dev.csv")
    df = transform.parse_dates(df, ['date'])
    df = transform.create_country_col(df)
    df.columns = ['area_code', 'area_name', 'area_type', 'date', 'new_cases_by_specimen_date', 'nation']
    return df

@pytest.fixture()
def pg_conn():
    if not os.getenv("PG_CONN_CRED"):
        dotenv.load_dotenv()
    PG_CONN_CRED = os.getenv("PG_CONN_CRED")
    return PG_CONN_CRED


def test_loading(df, pg_conn):
    dests = "olvsegun/covid_data_dev.cases_2"
    load.load_to_table(df, dests, pg_conn)
    schema, table = dests.split(".")
    engine = create_engine(pg_conn)
    with engine.connect() as conn:
        sql = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{schema}'
            AND table_name = '{table}';
        """
        return conn.execute(sql, schema, table).rowcount > 0
