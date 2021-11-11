CREATE TABLE IF NOT EXISTS "olvsegun/covid-data-uk-dev"."covid_model_join" (
    id TEXT,
    date date,
    area_code TEXT,
    area_name TEXT,
    area_type TEXT,
    nation TEXT,
    new_cases INTEGER,
    new_death INTEGER,
    vaccinations INTEGER
);

TRUNCATE TABLE "olvsegun/covid-data-uk-dev"."covid_model_join";

INSERT INTO "olvsegun/covid-data-uk-dev"."covid_model_join"
    SELECT
        c.id,
        c.date,
        c.area_code,
        c.area_name,
        c.area_type,
        c.nation,
        c.new_cases,
        d.new_death,
        v.vaccinations
    FROM "olvsegun/covid-data-uk-dev"."cases" AS c
    LEFT JOIN "olvsegun/covid-data-uk-dev"."deaths" AS d
        ON c.id = d.id
    LEFT JOIN "olvsegun/covid-data-uk-dev"."vaccinations" AS v
        ON c.id = v.id
   ORDER BY c.date DESC, c.area_code ASC;