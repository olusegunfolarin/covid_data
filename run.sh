#!/bin/bash
source covid-env/bin/activate
cd main_pipeline
python main.py -name cases -transform -validate  'https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&format=csv' olvsegun/covid_data_dev.cases
python main.py -name deaths -transform -validate  'https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newDeaths28DaysByDeathDate&format=csv' olvsegun/covid_data_dev.deaths
python main.py -name vaccinations -transform -validate  'https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newPeopleVaccinatedCompleteByVaccinationDate&format=csv' olvsegun/covid_data_dev.vaccinations
# python sql_executor.py ca_covid_data.sql