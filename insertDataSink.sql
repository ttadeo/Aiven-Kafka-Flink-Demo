execute statement
set
    begin
    -- Insert into on-time flights table
INSERT INTO
    on_time_flights
SELECT *
FROM flights
WHERE
    status = 'on_time';
-- Insert into delayed flights table
INSERT INTO
    delayed_flights
SELECT *
FROM flights
WHERE
    status IN ('delayed', 'cancelled');

end