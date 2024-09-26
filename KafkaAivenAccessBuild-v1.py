import uuid
import random
from datetime import datetime, timedelta
import json
from kafka import KafkaProducer

# Kafka server URL placeholder for SSL authentication
KAFKA_SERVER = 'your_kafka_server_url'

# Placeholder for client private key, client certificate, and CA certificate content
CLIENT_PRIVATE_KEY = b"""
-----BEGIN PRIVATE KEY-----
# Your private key here
-----END PRIVATE KEY-----
"""

CLIENT_CERT = b"""
-----BEGIN CERTIFICATE-----
# Your client certificate here
-----END CERTIFICATE-----
"""

CA_CERT = b"""
-----BEGIN CERTIFICATE-----
# Your CA certificate here
-----END CERTIFICATE-----
"""

# Write the certificates and private key to temporary files
# These files are necessary for Kafka's SSL authentication setup
with open('client_key.pem', 'wb') as key_file:
    # Write the client private key to a file
    key_file.write(CLIENT_PRIVATE_KEY)

with open('client_cert.pem', 'wb') as cert_file:
    # Write the client certificate to a file
    cert_file.write(CLIENT_CERT)

with open('ca_cert.pem', 'wb') as ca_file:
    # Write the CA certificate to a file
    ca_file.write(CA_CERT)

# Set up the Kafka producer with SSL authentication
# This producer will be used to send messages to a Kafka topic
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    security_protocol="SSL",  # Use SSL for secure communication
    ssl_cafile='ca_cert.pem',  # Path to CA certificate
    ssl_certfile='client_cert.pem',  # Path to client certificate
    ssl_keyfile='client_key.pem',  # Path to private key file
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize the message as JSON
)

def produce_flight_data():
    """
    Generate flight event data with randomized attributes:
    - Flight ID
    - Airline
    - Departure and arrival airports
    - Departure and arrival times
    - Flight status
    """
    flight_data = {
        "flight_id": str(uuid.uuid4()),  # Unique flight ID
        "airline": random.choice(["Delta", "United", "American Airlines"]),  # Random airline
        "departure_airport": random.choice(["JFK", "LAX", "ORD"]),  # Random departure airport
        "arrival_airport": random.choice(["ATL", "SFO", "DFW"]),  # Random arrival airport
        "departure_time": (datetime.utcnow() + timedelta(hours=random.randint(1, 10))).isoformat(),  # Departure time in the next 1-10 hours
        "arrival_time": (datetime.utcnow() + timedelta(hours=random.randint(11, 20))).isoformat(),  # Arrival time in the next 11-20 hours
        "status": random.choice(["on_time", "delayed", "cancelled"])  # Random flight status
    }
    return flight_data

# Continuously send flight events to the Kafka topic 'flights-topic'
# This loop simulates an ongoing stream of flight event data
while True:
    flight_event = produce_flight_data()  # Generate a new flight event
    producer.send('flights-topic', value=flight_event)  # Send the event to Kafka
    print(f"Produced: {flight_event}")  # Log the produced flight event
