import pytest
import pandas as pd
from main_pipeline.extract import get_csv_from_requests





@pytest.mark.parametrize("url, outcome", [
    ("https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&format=csv", 0),
    ("https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newDeaths28DaysByDeathDate&format=csv", 0)

]
)


def test_get_data(url, outcome):
    df = get_csv_from_requests(url)
    assert df.shape[0] > outcome