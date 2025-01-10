import pika, sys, os , time
from pymongo import MongoClient
import gridfs
from convert import to_mp3
import logging

logging.basicConfig(level=logging.INFO)  # Adjust the level to DEBUG for more detailed logs
logger = logging.getLogger(__name__)
def main():
    client=MongoClient("mongodb://host.docker.internal:27017")
    db_videos=client.videos
    db_mp3=client.mp3
    ## gridfs
    fs_videos=gridfs.GridFS(db_videos)
    fs_mp3=gridfs.GridFS(db_mp3)
    
    ##rabbitmq
    connection= pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',heartbeat=300))
    channel=connection.channel()
    
    def callback(ch,method,properties,body):
        
        err=to_mp3.start(body,fs_videos,fs_mp3,ch)
        if err:
            logger.error("basic Nack has been sent beacuse error happend while ")
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            logger.info(f"basic acknowledgemt has been sent to the video queue insdie main function in consumer.py")
            ch.basic_ack(delivery_tag=method.delivery_tag)
         
         
    
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"),
        on_message_callback=callback
    )
    
    print("Waiting fro messages. to exit press CTRL+c")
    
    channel.start_consuming()
    
    
if __name__== "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("interuptted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
        
        
    