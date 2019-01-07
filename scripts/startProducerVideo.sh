#!/bin/bash
echo "### Starting Producer ###"
cd ~/KafkaStreamingDemo/
. env/bin/activate
python producer/producer.py '~/Coco.2017.720p.BluRay.x264-[YTS.AG].mp4'
