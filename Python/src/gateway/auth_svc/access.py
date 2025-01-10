import os,requests

def login(request):
    auth=request.authorization
    if not auth:
        return None, ("missing credentials",401)
    basicAuth=(auth.username,auth.password)
    #os.environ.get here the environment varibale value will be specified 
    # in the kubenrets env configuration file which is the config .yaml file 
    #from there it will get the ip addres of that container 
    response=requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login"
        ,
        auth=basicAuth
    )
    
    if response.status_code==200:
        return response.text , None
    else:
        return None,(response.text,response.status_code)
    
