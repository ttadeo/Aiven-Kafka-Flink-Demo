 CREATE TABLE flights (
       flight_id STRING,
       airline STRING,
       departure_airport STRING,
       arrival_airport STRING,
       departure_time STRING,
       arrival_time STRING,
       status STRING
   ) WITH (
       'connector' = 'kafka',
       'topic' = 'flights-topic',
       'properties.bootstrap.servers' = 'kafka-2eef0cd8-timthecoder-demo-prep.l.aivencloud.com:14844',
       'format' = 'json',
       'scan.startup.mode' = 'earliest-offset'
   )