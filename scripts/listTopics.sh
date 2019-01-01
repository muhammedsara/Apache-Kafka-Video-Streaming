#!/bin/bash
echo "### Listing Kafka Topics###"
cd /opt/Kafka/kafka_2.11-2.1.0/
sudo bin/kafka-topics.sh --zookeeper localhost:2181 --list
