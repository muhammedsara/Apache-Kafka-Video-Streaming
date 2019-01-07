import os
import time
#import datetime
from threading import Thread
from flask import Flask, Response, render_template
from kafka import KafkaConsumer

# Fire up the Kafka Consumer
topics = ["webcam", "video"]
servers=['localhost:9092']
consumers = []
buffer = []
for topic in topics:
    consumers.append(KafkaConsumer(topic, bootstrap_servers=servers))
    # Frame Buffer
    buffer.append(b'')

# Set the consumer in a Flask App
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/webcam_feed', methods=['GET'])
def webcam_feed():
    return Response(get_video_stream(topic = 0),
               mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed', methods=['GET'])
def video_feed():
    """
    This is the heart of our video display. Notice we set the mimetype to 
    multipart/x-mixed-replace. This tells Flask to replace any old images with 
    new values streaming through the pipeline.
    """

    return Response(get_video_stream(topic = 1), 
               mimetype='multipart/x-mixed-replace; boundary=frame')

def get_video_stream(topic):
    """
    Here is where we recieve streamed images from the Kafka Server and convert 
    them to a Flask-readable format.
    """

    while True:
        time.sleep(0.04) #0.2=5fps, 0.04=25fps
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + buffer[topic] + b'\r\n\r\n')

def consumer_thread(topic, delay = 3):
    global topics
    global buffer
    index = topics.index(topic)
    while True:
        for msg in consumers[index]:
            buffer[index] = msg.value
        time.sleep(delay)

if __name__ == "__main__":
    threads = []
    for topic in topics:
        threads.append(Thread(target=consumer_thread,args=(topic,)))
    for t in threads:
        t.start()
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
