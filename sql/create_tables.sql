CREATE TABLE IF NOT EXISTS cdc_places_health_indicators (
    year INTEGER,
    stateabbr VARCHAR(10),
    statedesc VARCHAR(100),
    locationname VARCHAR(255),
    datasource VARCHAR(100),
    category VARCHAR(255),
    measure TEXT,
    data_value FLOAT,
    data_value_unit VARCHAR(50),
    data_value_type VARCHAR(100),
    low_confidence_limit FLOAT,
    high_confidence_limit FLOAT,
    totalpopulation INTEGER,
    geolocation TEXT
);
