import os,requests
import logging

logging.basicConfig(level=logging.INFO)  # Adjust the level to DEBUG for more detailed logs
logger = logging.getLogger(__name__)
def tokenValidation(request):
    if not "Authorization" in request.headers:
        return None ,('missing credentials',401)
    token=request.headers['Authorization']
    
    if not token:
        return None ,('missing credentials',401)
    
    response=requests.post( 
    f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
    headers={"Authorization":token})
    
    if response.status_code==200:
        return response.text ,None
    else:
        return None ,('invalid token',401)
        
    
    