#!/bin/bash
echo "### Starting Consumer ###"
cd ~/KafkaStreamingDemo/
. env/bin/activate
python consumer/consumer.py

