#!/bin/bash
source covid-env/bin/activate
cd main_pipeline
# Uncomment the line below if you would like to re-run the population data pipeline
# The population data is updated annually by the Census Bureau and does not need to re-run daily
# python main.py -local_source -name acs_population_counties acs_5yr_population_data.csv bitdotio/simple_pipeline.population_counties
python main.py -name cases -transform -validate  'https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&format=csv' olvsegun/covid_data_dev.cases
python main.py -name deaths -transform -validate  'https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newDeaths28DaysByDeathDate&format=csv' olvsegun/covid_data_dev.deaths
python main.py -name vaccinations -transform -validate  'https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newPeopleVaccinatedCompleteByVaccinationDate&format=csv' olvsegun/covid_data_dev.vaccinations
# python sql_executor.py ca_covid_data.sql