-- Create Table for the divvy_trips dataset
CREATE TABLE divvy_trips (
    ride_id VARCHAR PRIMARY,
    rideable_type VARCHAR,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    start_station_name VARCHAR,
    start_station_id VARCHAR,
    end_station_name VARCHAR,
    end_station_id VARCHAR,
    start_lat, FLOAT
    start_lng FLOAT,
    end_lat FLOAT,
    end_lng FLOAT,
    member_casual VARCHAR,
);
COPY divvy_trips
FROM '/Chicago-Transit-Analysis/2025jan_divvy.csv'
DELIMITER ','
CSV HEADER;




