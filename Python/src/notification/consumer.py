import pika, sys, os , time
from send import email
import logging

logging.basicConfig(level=logging.INFO)  # Adjust the level to DEBUG for more detailed logs
logger = logging.getLogger(__name__)
def main():
    
    ##rabbitmq
    connection= pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',heartbeat=300))
    channel=connection.channel()
    
    def callback(ch,method,properties,body):
        
        err=email.notification(body)
        if err:
            logger.error("basic Nack has been sent beacuse error happend while ")
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            logger.info(f"basic acknowledgemt has been sent to the mp3 queue insdie main function in consumer.py of notifocation")
            ch.basic_ack(delivery_tag=method.delivery_tag)
         
         
    
    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"),
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
        
        
    