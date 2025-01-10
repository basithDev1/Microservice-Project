import smtplib, os ,json
from email.message import EmailMessage
import logging

logging.basicConfig(level=logging.INFO)  # Adjust the level to DEBUG for more detailed logs
logger = logging.getLogger(__name__)
def notification(message):
    try:
        message=json.loads(message)
        mp3_fid=message["mp3_fid"]
        sender_address=os.environ.get("GMAIL_ADDRESS")
        sender_password=os.environ.get("GMAIL_PASSWORD")
        receiver_address=message["username"]
        
        msg=EmailMessage()
        msg.set_content(f"the fid of the mp3 is {mp3_fid}")
        msg["Subject"]="MP3 DOWLOAD"
        msg["FROM"]=sender_address
        msg["TO"]=receiver_address
    
        session=smtplib.SMTP("smtp.gmail.com")
        session.starttls()
        session.login(sender_address, sender_password)
        session.send_message(msg,sender_address,receiver_address)
        session.quit()
        logger.info("the email has been sended succesfully")
        return False
    except  Exception as err :
        logger.error(f"Error sending email: {err}")
        return True
        