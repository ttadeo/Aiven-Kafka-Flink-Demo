 CREATE TABLE on_time_flights (
       flight_id STRING,
       airline STRING,
       departure_airport STRING,
       arrival_airport STRING,
       departure_time STRING,
       arrival_time STRING
   ) WITH (
       'connector' = 'kafka',
       'topic' = 'on-time-flights-topic',  -- Ensure this topic exists
       'properties.bootstrap.servers' = 'kafka-2eef0cd8-timthecoder-demo-prep.l.aivencloud.com:14844',
       'format' = 'json'
   );