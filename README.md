# Apache-Kafka-Video-Streaming

 
## KURULUM

Kurulum işlemi Ubuntu 16.04 üzerinden yapılmıştır.

#### Başlarken
 > Aşağıdaki komutu çalıştırarak sunucunuzu güncelleyin

```shell
$ sudo apt-get update -y
$ sudo apt-get upgrade -y
```
---

### Java Kurulum

> Kafka'yı kurmadan önce Java'yı sisteminize kurmanız gerekecektir. Webupd8 daki PPA  kullanarak Oracle JDK 8'i yükleyebilirsiniz.

> Repository eklemek için aşağıdaki komutu çalıştırın

```shell
$ sudo add-apt-repository -y ppa:webupd8team/java
```



> Aşağıdaki çıktıyı görmelisiniz

```shell
gpg: keyring `/tmp/tmpkjrm4mnm/secring.gpg' created
gpg: keyring `/tmp/tmpkjrm4mnm/pubring.gpg' created
gpg: requesting key EEA14886 from hkp server keyserver.ubuntu.com
gpg: /tmp/tmpkjrm4mnm/trustdb.gpg: trustdb created
gpg: key EEA14886: public key "Launchpad VLC" imported
gpg: no ultimately trusted keys found
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)
OK
```

> Ardından, aşağıdaki komutu çalıştırarak yeni repository meta verilerini güncelleyin

```shell
$ sudo apt-get update
```

> İşlem bittiğınde, JDK 8'i yüklemek için aşağıdaki komutu çalıştırın

```shell
$ sudo apt-get install oracle-java8-installer -y
```

> Aşağıdaki komutu çalıştırarak JDK 8'in düzgün şekilde yüklendiğini de doğrulayabilirsiniz.
```shell
$ sudo java -version
```

> Çıktıyı bu şekilde görmelisiniz

```shell
java version "1.8.0_66"
Java(TM) SE Runtime Environment (build 1.8.0_66-b17)
Java HotSpot(TM) 64-Bit Server VM (build 25.66-b17, mixed mode)
```

---

#### ZooKeeper Kurulumu

> Apache Kafka'yı kurmadan önce, ZooKeeper hazır ve çalışıyor olması gerekir. ZooKeeper, yapılandırma bilgilerini korumak, dağıtılmış senkronizasyon sağlamak, grup hizmetleri adlandırmak ve sağlamak için açık kaynaklı bir hizmettir.


> Varsayılan olarak ZooKeeper paketi Ubuntu'nun varsayılan repositorysinde bulunur, aşağıdaki komutu çalıştırarak kurabilirsiniz

```shell
$ sudo apt-get install zookeeperd
```

> Kurulum tamamlandığında, otomatik olarak bir daemon olarak başlatılacaktır. ZooKeeper varsayılan olarak 2181 numaralı bağlantı noktasında çalışacaktır.

>  Aşağıdaki komutu çalıştırarak test edebilirsiniz.

```shell
netstat -ant | grep :2181
```

> Her şey yolundaysa, aşağıdaki Çıktıyı görmelisiniz

```shell
tcp6       0      0 :::2181                 :::*                    LISTEN
```


---
#### Kafka Sunucu Kurulumu ve Başlatma



> Artık Java ve ZooKeeper yüklendiğine göre, Kafka'yı Apache web sitesinden indirip çıkarmanın zamanı geldi. Kafka'yı indirmek için wget kullanabilirsiniz.

```shell
$ wget http://ftp.itu.edu.tr/Mirror/Apache/kafka/2.1.0/kafka_2.11-2.1.0.tgz
```

> Ardından, Kafka kurulumu için bir dizin oluşturun

```shell
$ sudo mkdir /opt/Kafka
```

> İndirilen arşivi /opt/Kafka dizinindeki tar komutunu kullanarak açın

```shell
$ sudo tar -xvf kafka_2.11-2.1.0.tgz -C /opt/Kafka/
```

> Bir sonraki adım Kafka sunucusunu başlatmak,  /opt/Kafka/kafka_2.10-0.10.0.1/bin/ dizininde bulunan kafka-server-start.sh scriptini çalıştırarak başlatabilirsiniz.

```shell
$ cd /opt/Kafka/kafka_2.11-2.1.0/
$ sudo  bin/kafka-server-start.sh config/server.properties
```

> Sunucu başarıyla başlatılmışsa, aşağıdaki çıktıyı görmelisiniz


```shell
[2016-08-22 21:43:48,279] WARN No meta.properties file under dir /tmp/kafka-logs/meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2016-08-22 21:43:48,516] INFO Kafka version : 0.10.0.1 (org.apache.kafka.common.utils.AppInfoParser)
[2016-08-22 21:43:48,525] INFO Kafka commitId : a7a17cdec9eaa6c5 (org.apache.kafka.common.utils.AppInfoParser)
[2016-08-22 21:43:48,527] INFO [Kafka Server 0], started (kafka.server.KafkaServer)
[2016-08-22 21:43:48,555] INFO New leader is 0 (kafka.server.ZookeeperLeaderElector$LeaderChangeListener)
```

> Her şeyin çalışır durumda olduğunu test edin, yeni bir terminal açıp aşağıdaki komutları deneyin

```shell
$ sudo bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1  --partitions 1 --topic testing
```
> Aşağıdaki gibi cıktı alınmalıdır
```shell
Created topic "testing".
```

> Kafka sunucusunu arka plan işlemi olarak başlatmak için nohup komut dosyasını komut ile kullanabilirsiniz.
```shell
$ sudo nohup /opt/Kafka/kafka_2.10-0.10.0.1/bin/kafka-server-start.sh /opt/Kafka/kafka_2.11-2.1.0/config/server.properties /tmp/kafka.log 2>&1 &
```

> Artık 9092 numaralı bağlantı noktasında çalışan ve dinleyen bir Kafka sunucunuz var.

---

#### Testing Kafka Server

> Öncelikle projemiz için yeni bir dizin oluşturacağız.

```shell
$ mkdir kafkaDemo 
$ cd kafkaDemo
```

> Sanal ortamımızı çalıştırıyoruz.
```shell
$ virtualenv env
$ . env/bin/activate
```
 Kafka client çalışır duruma getirmek Kafka-Python projesine ihtiyacımız var.

> Ayrıca, video dağıtımı için OpenCV'a ve “dağıtılmış” Consumer için Flask'a ihtiyacımız olacak.
```shell
$ pip install kafka-python opencv-contrib-python Flask
```

 Son bölümde kurduğumuz Kafka Sunucusu 9092 numaralı portuna bağlı. İki Kafka clientini kurarken bu değeri kullanacağız.



### Producer

Kafka clientinin ilki, producer mesajı olacaktır. Burada videoyu bir JPEG görüntü akışına dönüştürmek işlemi yapılacaktır. 

```javascript
import sys
import time
import cv2
from kafka import KafkaProducer

servers=['localhost:9092']

def publish_video(video_file):
    """
    Publish given video file to a specified Kafka topic. 
    Kafka Server is expected to be running on the localhost. Not partitioned.
    
    :param video_file: path to video file <string>
    """
    # Start up producer
    producer = KafkaProducer(bootstrap_servers=servers)

    # Open file
    video = cv2.VideoCapture(video_file)
    
    print('publishing video...')

    while(video.isOpened()):
        success, frame = video.read()

        # Ensure file was read successfully
        if not success:
            print("bad read!")
            break
        
        # Convert image to png
        ret, buffer = cv2.imencode('.jpg', frame)

        # Convert to bytes and send to kafka
        producer.send("video", buffer.tobytes())

        time.sleep(0.04)
    video.release()
    print('publish complete')

def publish_camera():
    """
    Publish camera video stream to specified Kafka topic.
    Kafka Server is expected to be running on the localhost. Not partitioned.
    """

    # Start up producer
    producer = KafkaProducer(bootstrap_servers=servers)

    
    camera = cv2.VideoCapture(0)
    try:
        while(True):
            success, frame = camera.read()
        
            ret, buffer = cv2.imencode('.jpg', frame)
            producer.send("webcam", buffer.tobytes())
            
            # Choppier stream, reduced load on processor
            time.sleep(0.2)

    except:
        print("\nExiting.")
        sys.exit(1)

    
    camera.release()


if __name__ == '__main__':
    """
    Producer will publish to Kafka Server a video file given as a system arg. 
    Otherwise it will default by streaming webcam feed.
    """
    if(len(sys.argv) > 1):
        video_path = sys.argv[1]
        publish_video(video_path)
    else:
        print("publishing feed!")
        publish_camera()
```
Producer doğrudan bir web kamerasından video akışı yaparak varsayılan ayarlara sahiptir; Bir video dosyasından çekme, stiliniz daha fazlaysa, Producer bir dosya adını komut satırı argümanı olarak kabul eder.


### Consumer

Yeni yayınlanan akışımızı okumak için Kafka konusuna erişen bir Consumer'e ihtiyacımız olacak. Mesaj akış sistemimiz dağıtık bir sistem için tasarlandığından, projemizi bu bölüm içinde tutacağız ve Tüketici'yi Flask servisi olarak açacağız.


```javascript
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


```

### Projenin Çalıştırılması

Şimdi her şeyi bir araya getirireceğiz. Sırasıyla, Kafka'yı, Consumer'i ve nihayetinde Prducer'i, her birinin kendi terminalinde başlatlır.

> Kafka' yı başlatcağız

```shell
$ cd /opt/Kafka/kafka_2.11-2.1.0/
$ sudo  bin/kafka-server-start.sh config/server.properties
```

> Yeni bir terminalde sanal ortamını ve Consumer projesini başlatacağız.


```shell
$ cd ~/KafkaDemo
$ . env/bin/activate
$ python consumer.py
```

> Her şey çalışıyorsa terminaliniz okumalısınız

```shell
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

> Tarayıcıda, http://0.0.0.0:5000/video adresine gidin. Burada henüz bir şey görmeyeceksin, bir kaç adım sonra gelecek

> Consumer için de aynı. İlk önce yeni bir terminal açın. Burada, web kamerasından akış yapacağız, bu nedenle ek argümana gerek yok.

```shell
$ cd ~/KafkaDemo
$ . env/bin/activate
$ python producer.py

```

> Kısa bir video yayınlamak istiyorsak, son komutu aşağıdaki gibi yazabiliriz.
```shell
python producer.py videos/Countdown1.mp4
```






