import numpy as np
import pandas as pd
import requests
import base64
import os
import json

#################### Get client id ####################
client_id = os.environ['CLIENT_ID']
client_secret = os.environ.get('CLIENT_SECRET')
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}
message = f"{client_id}:{client_secret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')
headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)
print(r)