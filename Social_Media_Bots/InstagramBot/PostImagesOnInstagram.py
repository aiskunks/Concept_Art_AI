from dotenv import load_dotenv
import os
load_dotenv()
import requests
import http.server
import socketserver
import threading
import subprocess
import time
import json

'''
This feature is still in development, but the main logic of the code works!
# Start a simple HTTP server in a new thread
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
thread = threading.Thread(target=httpd.serve_forever)
thread.start()

# Start ngrok
ngrok = subprocess.Popen(["ngrok", "http", str(PORT)], stdout=subprocess.PIPE)

# Give ngrok time to start up
time.sleep(2)

# Get the public URL from ngrok
resp = requests.get("http://localhost:4040/api/tunnels")
public_url = resp.json()["tunnels"][0]["public_url"]

# Now you can use the public URL to access your local images

'''
# Instagram
username = os.getenv('INSTA_USERNAME')
password = os.getenv('INSTA_PASSWORD')
insta_user_id = os.getenv('INSTA_USER_ID')
app_secret = os.getenv("APP_SECRET")
app_id = os.getenv("APP_ID")
redirect_uri = "http://localhost:5000"
access_token = os.getenv("ACCESS_TOKEN")

graph_url = 'https://graph.facebook.com/v18.0/'
image_url= "/Images/mufasa_edited.png" # put your image name here that you copied to Images folder

# URL using ngrok: public url + image_url 
caption = "#Pattern"

def create_container(caption='', image_url='',instagram_account_id='',access_token=''):
    url = graph_url + instagram_account_id + '/media'
    param = dict()
    param['access_token'] = access_token
    param['caption'] = caption
    param['image_url'] = image_url
    response = requests.post(url, params=param)
    response = response.json()
    return response

def publish_container(creation_id = '',instagram_account_id='',access_token=''):
    url = graph_url + instagram_account_id + '/media_publish'
    param = dict()
    param['access_token'] = access_token
    param['creation_id'] = creation_id
    response = requests.post(url,params=param)
    response = response.json()
    return response

def status_of_upload(ig_container_id = '',access_token=''):
    url = graph_url + ig_container_id
    param = {}
    param['access_token'] = access_token
    param['fields'] = 'status_code'
    response = requests.get(url,params=param)
    response = response.json()
    return response

container_id = create_container(caption=caption, image_url=image_url, instagram_account_id=insta_user_id, access_token=access_token)
print(container_id)

result = publish_container(creation_id=container_id.get("id"), instagram_account_id=insta_user_id, access_token=access_token)
print(result)

status = status_of_upload(ig_container_id=container_id.get("id"), access_token=access_token)
print(status)