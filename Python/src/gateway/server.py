import os,gridfs,pika,json
from flask import Flask,request, send_file
from flask_pymongo import PyMongo
from flask import jsonify
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId
import logging

logging.basicConfig(level=logging.INFO)  # Adjust the level to DEBUG for more detailed logs
logger = logging.getLogger(__name__)


server=Flask(__name__)

mongo_video= PyMongo(server,uri='mongodb://host.docker.internal:27017/videos')
mongo_mp3= PyMongo(server,uri='mongodb://host.docker.internal:27017/mp3')

fs_videos=gridfs.GridFS(mongo_video.db)
fs_mp3=gridfs.GridFS(mongo_mp3.db)


connection=pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq",heartbeat=300))
channel=connection.channel()



@server.route("/login",methods=["POST"])
def login():
    print("Request received at /login")
    token,err=access.login(request)
    
    if not err:
        print("token returned")
        return token
    else:
        jsonify({"error": "Error from gateway login side", "details": err}), 400  # Return error with status code
    
@server.route("/upload",methods=['POST'])
def upload():
    decodeToken, err=validate.tokenValidation(request)
    
    if decodeToken is None:
        logger.info("here the decoded token is none retuned gateway /upload")
        return jsonify({"error": "Error from gateway upload side, no decoded token recievd", "details": err}), 400
    
    decodeToken=json.loads(decodeToken)
    logger.info(f"the decoded token is {decodeToken} from gateway /upload")
    if decodeToken['admin']:
        if len(request.files)>1 or len(request.files)<1:
            return "Exactly 1 file is required",400
        
        for key,file in request.files.items():
            err=util.upload(file,fs_videos ,channel,decodeToken)
            
            if err:
                return err
        return "succes!", 200
    else:
        return "Not authorized",401
            
            
@server.route('/download',methods=['POST'])
def download():
    decodeToken, err=validate.tokenValidation(request)
    
    if decodeToken is None:
        logger.info("here the decoded token is none returned gateway /dowload")
        return jsonify({"error": "Error from gateway dowload side, no decoded token recievd", "details": err}), 400
    
    
    decodeToken=json.loads(decodeToken)
    logger.info(f"the decoded token is {decodeToken} from gateway /upload")
    if decodeToken['admin']:
        fid_string=request.args.get("fid")
        if not fid_string:
            logger.error("no fid found in request arguments, error at gateway /dowloads")
            return "fid is required",400    
        else:
            try:
                out=fs_mp3.get(ObjectId(fid_string))
                logger.info("succesful sende the audio mp3 to the client")
                return send_file(out,download_name=f'{fid_string}.mp3')
            except Exception as e:
                logger.error(f"this error occure at the catch block of gateway /dowload while trying to get the audio from mongo db using the fid the erro is : {e}")
                return jsonify({"error": "internal server error","details": err}), 500
    else:
        return "Not authorized",401
         
        
        
        
if __name__=="__main__":
    server.run(host="0.0.0.0",port=8080)    