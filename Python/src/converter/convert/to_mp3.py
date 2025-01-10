import pika,json,tempfile,os
from bson.objectid import ObjectId
from moviepy import VideoFileClip
import logging

logging.basicConfig(level=logging.INFO)  # Adjust the level to DEBUG for more detailed logs
logger = logging.getLogger(__name__)

def start(message,fs_videos,fs_mp3,channel):
    message=json.loads(message)
    logger.info(f"message is receive at to_mp3 start function id is : {message['video_fid']}")
    ###empty temp file
    
    tf= tempfile.NamedTemporaryFile()
    ##
    out= fs_videos.get(ObjectId(message["video_fid"]))
    
    tf.write(out.read())
    audio= VideoFileClip(tf.name).audio
    tf.close()
    
    ## tf_path=tempfile.gettempdir() + f"/{message["video_fid"]}.mp3"
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"

    audio.write_audiofile(tf_path)
    
    ##save to mongo
    f=open(tf_path,"rb")  
    data=f.read()
    try:
        logger.info(f"putting mp3 into mp3 database inside to_mp3 start function")
        fid=fs_mp3.put(data)
    except Exception as err:
        logger.error(f"Error putting mp3 into mp3 database inside to_mp3 start function")
        return err
    f.close()
    os.remove(tf_path)
    
    message['mp3_fid']=str(fid)
    
    try:
        channel.basic_publish(
            exchange='',
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        logger.info("succesfully converted into mp3 and pushed meessage into ques")
        return False
    except Exception as err:
        logger.error(f"Error putting message to mp3 queue inside to_mp3 start function")
        fs_mp3.delete(fid)
        return True