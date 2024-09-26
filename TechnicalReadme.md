

```

```---

### **Aiven Step-by-Step Guide: Using Aiven for Kafka and Flink**

---

### **Step 1: Set Up Kafka in Aiven**
1. **Create a Kafka Service on Aiven**:
   - Log in to your **Aiven Console**.
   - Navigate to **Create New Service** and select **Apache Kafka**.
   - Configure your Kafka service (select cloud provider, region, and plan).
   - Once the Kafka service is up, note the **Service URI**, **Host**, and **Port** (e.g., kafka-2eef0cd8-timthecoder-demo-prep.l.aivencloud.com:14844).

2. **Create Kafka Topics**:
   To ensure data can be written from Flink to Kafka, you must create the following topics:
   - **`flights-topic`**: For incoming flight data.
   - **`on-time-flights-topic`**: For on-time flights.
   - **`delayed-flights-topic`**: For delayed or cancelled flights.

   You can create these topics through the Aiven Console:
   - Navigate to **Topics** in your Kafka service.
   - Click **Create Topic** for each topic, specifying the name and desired configurations (e.g., partitions and replication factor).

   Alternatively, use the Kafka command-line tool (if available):
   ```bash
   kafka-topics.sh --create --topic flights-topic --bootstrap-server kafka-2eef0cd8-timthecoder-demo-prep.l.aivencloud.com:14844 --replication-factor 1 --partitions 1

   kafka-topics.sh --create --topic on-time-flights-topic --bootstrap-server kafka-2eef0cd8-timthecoder-demo-prep.l.aivencloud.com:14844 --replication-factor 1 --partitions 1

   kafka-topics.sh --create --topic delayed-flights-topic --bootstrap-server kafka-2eef0cd8-timthecoder-demo-prep.l.aivencloud.com:14844 --replication-factor 1 --partitions 1
   ```

---

### **Step 2: Set Up Security and Download Credentials**
1. **Download the Client Certificates**:
   - In the **Aiven Console**, go to your Kafka service details and download the following certificates:
     - **Client Certificate (client_cert.pem)**
     - **Client Private Key (client_key.pem)**
     - **CA Certificate (ca_cert.pem)**

   Save these files in the same directory as your **KafkaAivenAccessBuild.py** script.

2. **Configure Kafka ACLs**:
   - Ensure that you’ve set appropriate **Kafka ACLs** to allow the producer to publish messages to the `flights-topic`.

---

### **Step 3: Write and Run the Kafka Producer (KafkaAivenAccessBuild.py)**

#### **KafkaAivenAccessBuild.py**:
```python
import uuid
import random
from datetime import datetime, timedelta
import json
from kafka import KafkaProducer

# Aiven Kafka connection details
KAFKA_SERVER = 'kafka-2eef0cd8-timthecoder-demo-prep.l.aivencloud.com:14844'

# Set up the Kafka producer with SSL authentication and JSON serializer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    security_protocol="SSL",
    ssl_cafile='ca_cert.pem',      # CA certificate file
    ssl_certfile='client_cert.pem', # Client certificate file
    ssl_keyfile='client_key.pem',   # Client private key file
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Ensures data is sent as JSON
)

# Function to generate random flight data
def produce_flight_data():
    flight_data = {
        "flight_id": str(uuid.uuid4()),  # Unique flight ID
        "airline": random.choice(["Delta", "United", "American Airlines"]),  # Random airline
        "departure_airport": random.choice(["JFK", "LAX", "ORD"]),  # Random departure airport
        "arrival_airport": random.choice(["ATL", "SFO", "DFW"]),  # Random arrival airport
        "departure_time": (datetime.utcnow() + timedelta(hours=random.randint(1, 10))).isoformat(),  # Random departure time
        "arrival_time": (datetime.utcnow() + timedelta(hours=random.randint(11, 20))).isoformat(),  # Random arrival time
        "status": random.choice(["on_time", "delayed", "cancelled"])  # Random status
    }
    return flight_data

# Continuous loop to send flight events to Kafka topic 'flights-topic'
while True:
    flight_event = produce_flight_data()  # Generate flight data
    producer.send('flights-topic', value=flight_event)  # Send data to Kafka topic
    print(f"Produced: {flight_event}")  # Print confirmation of the produced message
```

---

### **Step 4: Run the Kafka Producer**
1. **Prepare the Kafka Producer**:
   - Save the above script as **`KafkaAivenAccessBuild.py`**.
   - Ensure that the SSL certificates (`client_cert.pem`, `client_key.pem`, `ca_cert.pem`) are saved in the same directory as the script.

2. **Run the Script**:
   In your terminal, navigate to the directory where the script and certificates are located and run the producer:
   ```bash
   python3 KafkaAivenAccessBuild.py
   ```

3. **Verify Kafka Messages**:
   - The script continuously generates random flight data and sends it to the Kafka topic **`flights-topic`**.
   - In the Aiven Console, navigate to **Kafka service -> Topics -> flights-topic** and fetch the messages to verify the data.

---

### **Step 5: Set Up Flink in Aiven**
1. **Create a Flink Service on Aiven**:
   - In the Aiven Console, navigate to **Create New Service** and select **Apache Flink**.
   - Configure the service as per your requirements.

2. **Create an SQL Application in Flink**:
   - In the Aiven Console, go to the Flink service and create a SQL application for processing the data from Kafka.

---

### **Step 6: Write and Deploy Flink SQL for Data Processing**

#### **SQL Queries for Flink Job**:
1. **Create the Source Table for Kafka Data**:
   This table reads data from the Kafka topic (`flights-topic`), which receives flight data from the Kafka producer.
   ```sql
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
   );
   ```

2. **Create Output Tables**:
   Split the data into two Kafka topics based on flight status (on_time and delayed/cancelled).
   - Create a table for on-time flights:
   ```sql
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
   ```

   - Create a table for delayed/cancelled flights:
   ```sql
   CREATE TABLE delayed_flights (
       flight_id STRING,
       airline STRING,
       departure_airport STRING,
       arrival_airport STRING,
       departure_time STRING,
       arrival_time STRING,
       status STRING
   ) WITH (
       'connector' = 'kafka',
       'topic' = 'delayed-flights-topic',  -- Ensure this topic exists
       'properties.bootstrap.servers' = 'kafka-2eef0cd8-timthecoder-demo-prep.l.aivencloud.com:14844',
       'format' = 'json'
   );
   ```

3. **Insert Processed Data into Output Tables**:
   This splits the incoming flight data into two separate Kafka topics.
   ```sql
   -- Insert into on-time flights table
   INSERT INTO on_time_flights
   SELECT flight_id, airline, departure_airport, arrival_airport, departure_time, arrival_time
   FROM flights
   WHERE status = 'on_time';

   -- Insert into delayed flights table
   INSERT INTO delayed_flights
   SELECT flight_id, airline, departure_airport, arrival_airport, departure_time, arrival_time, status
   FROM flights
   WHERE status IN ('delayed', 'cancelled');
   ```

4. **Deploy the SQL Job**:
   - Run the above SQL statements in the Flink dashboard to deploy the Flink SQL job.
   - This job will split flight data based on its status into two Kafka topics: `on-time-flights-topic` and `delayed-flights-topic`.

---

### **Step 7: Verify the Data Flow**
1. **Check Kafka Messages

**:
   - In the Aiven Console, navigate to the Kafka service and check the `flights-topic`, `on-time-flights-topic`, and `delayed-flights-topic`.
   - Ensure that the messages are being correctly processed and split into these topics based on the flight status.

---

### **Step 8: (Optional) Set Up Monitoring Using Grafana**
1. **Integrate Aiven with Grafana**:
   - Set up **Aiven for Grafana** and monitor metrics for your Kafka and Flink services.
   - You can monitor message throughput, consumer lag, and other metrics.

2. **View Dashboards**:
   - Use pre-built dashboards in Grafana to monitor your Kafka and Flink pipelines in real time.

---

### **Summary of Steps**:
1. **Set up Kafka in Aiven**: Create the Kafka service and topics (`flights-topic`, `on-time-flights-topic`, `delayed-flights-topic`).
2. **Run the Kafka Producer**: Use the **`KafkaAivenAccessBuild.py`** script to send flight data in JSON format.
3. **Set up Aiven Flink**: Create the Flink service and SQL application.
4. **Deploy Flink SQL Job**: Split the flight data into two topics based on flight status.
5. **Verify Data Flow**: Ensure the Kafka messages are correctly split and processed.
6. **(Optional) Set up Monitoring**: Use Grafana to monitor the Kafka-Flink pipeline.

---

