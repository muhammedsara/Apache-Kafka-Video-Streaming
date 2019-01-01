#!/bin/bash
echo "### Starting Kafka ###"
cd /opt/Kafka/kafka_2.11-2.1.0/
sudo bin/kafka-server-start.sh config/server.properties
