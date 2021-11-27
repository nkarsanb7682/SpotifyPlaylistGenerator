import numpy as np
import pandas as pd
import requests
import base64
import os
import json

url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

r = requests.post(url, headers=headers, data=data)

########## Get developer token
