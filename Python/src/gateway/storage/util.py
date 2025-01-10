import os,requests
import pika,json
import logging

logging.basicConfig(level=logging.INFO)  # Adjust the level to DEBUG for more detailed logs
logger = logging.getLogger(__name__)
def upload(file,fs,channel,decodeToken):
    try:
        fid=fs.put(file)
    except Exception as err:
        logger.info(f"this error happend in util.upload error is : {err}")
        return "internal server error",500
    
    message={
        "video_fid":str(fid),
        "username":decodeToken['username'],
        "mp3_fid":None
    }
    
    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                            )
        )
        logger.info("succesfuly uploaded and message pushed into ques")
        return "succesfuly uploaded and message pushed into ques", 200
    except:
        fs.delete(fid)
        logger.info("this erro happen in catch block of upload function ")
        return "internal server error",500
        
        