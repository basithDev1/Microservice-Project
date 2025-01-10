import jwt
import os
import datetime
from flask import Flask,request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask import jsonify
import logging

server=Flask(__name__)
mysql=MySQL(server)
server.config['MYSQL_HOST']=os.environ.get('MYSQL_HOST')
server.config['MYSQL_USER']=os.environ.get('MYSQL_USER')
server.config['MYSQL_PASSWORD']=os.environ.get('MYSQL_PASSWORD')
server.config['MYSQL_DB']=os.environ.get('MYSQL_DB')
server.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))



logging.basicConfig(level=logging.INFO)  # Adjust the level to DEBUG for more detailed logs
logger = logging.getLogger(__name__)



@server.route('/login',methods=['POST'])
def login():
    auth=request.authorization
    if not auth:
        return "missing credentials",401
    
    #check db for username and password
    cur=mysql.connection.cursor()
    res=cur.execute('SELECT email,password FROM user WHERE email=%s',(auth.username,)
                    )
    if res>0:
        user_row=cur.fetchone()
        print(user_row,'the result cur.fetchone')
        email=user_row[0]
        password=user_row[1]
    else:
        return "No user found",401
    
    if auth.username!=email or auth.password!=password:
        return "invalid credentials",401
    else:
        logger.info(f"the secret is when encoding {os.environ.get('JWT_SECRET')}")
        return createJWT(auth.username,os.environ.get("JWT_SECRET"),authz=True)


#HERE THE ACTUALY DECODING OF THE JWT WILL HAPPEN AND IF ITS NOT DECODE PROPERLY USNG THE SECRET AND ALGO THEN THAT MEAN ITS AN INVALID TOKEN
@server.route('/validate',methods=['POST'])
def validate():
    encoded_jwt = request.headers.get('Authorization')
    logger.info(f"the encoded jwt is {encoded_jwt}")
    if not encoded_jwt:
        return 'missing jwt in headder',401
    encoded_jwt=encoded_jwt.split(" ")[1]
    logger.info(f"the encoded jwt is : {encoded_jwt} from auth /validate")
    try:
       #IF ERROR CHECK UTBE 52:03 TIMESTAMP
      logger.info(f"the secret is when decoding is  {os.environ.get('JWT_SECRET')}")
      decode_jwt = jwt.decode(encoded_jwt,os.environ.get('JWT_SECRET'), algorithms=["HS256"])
      logger.info(f"the decoded jwtfrom the auth /validate {decode_jwt} try block")
    except:
        return 'not authorized',403
    logger.info("token succesfully validated from auth /validate")
    return decode_jwt,200




def createJWT(username,secret,authz):
    return jwt.encode(
        {
            "username":username,
            "exp":datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(days=1),
            "iat":datetime.datetime.now(datetime.timezone.utc),
            "admin":authz
        },
        secret,
        algorithm="HS256"
    )

if __name__=='__main__':
    server.run(port=5000,host='0.0.0.0')
    

    
