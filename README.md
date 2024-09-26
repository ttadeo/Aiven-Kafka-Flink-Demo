# Aiven-Kafka-Flink-Demo
 This repo contains all assets that are related to the demo
Aiven Kafka, Flink, and Observability Demo
This demo showcases the integration of Aiven Kafka, Aiven Flink, and Aiven Observability to build a real-time data processing pipeline using flight data. The key components of the demo include:

Kafka Producer: A Python script (KafkaAivenAccessBuild.py) generates random flight data and streams it to a Kafka topic (flights-topic) securely using SSL authentication.

Data Processing with Flink: The Aiven Flink service processes the incoming flight data in real-time. It filters the data based on flight status, splitting it into two distinct topics: on-time-flights-topic and delayed-flights-topic.

Observability: Integration with Aiven for Metrics allows for monitoring of the Kafka and Flink services, providing insights into data flow and system performance through Grafana dashboards.

This demo illustrates the power and ease of using Aiven's managed services to build scalable and efficient data pipelines, enabling organizations to derive real-time insights from their data.
