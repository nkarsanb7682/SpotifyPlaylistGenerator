from flask import Flask, request, Response
import os
import pika
import datetime
import random
import jsonpickle
import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import pickle
import urllib.request

rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"
print("Connecting to rabbitmq({})".format(rabbitMQHost))


# Info for client token
if os.environ['CLIENT_ID'] == None or os.environ.get('CLIENT_SECRET') == None:
    print("CLIENT_ID, and/or CLIENT_SECRET is None. Terminating server")
    quit()
else:
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ.get('CLIENT_SECRET')
spotifyClientTokenExpirationDate = datetime.datetime.now()
scope = "user-library-read user-follow-read user-top-read"
redirect_uri = 'http://localhost:5000/'

#################### Define flask app and routes ####################
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return '<h1> Playlist Generation Server</h1><p> User is logged in</p><p>Click <a href={}>here</a> to logout</p>'.format(redirect_uri + 'apiv1/logout')

@app.route(('/apiv1/login'), methods=['POST'])
def login():
    print("START OF LOGIN &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
    auth_url = sp_oauth.get_authorize_url()
    print("&&&&&&&&&&&&&&&&&&&&&&&&", urllib.request.urlopen(auth_url).read())
    code = sp_oauth.parse_response_code(auth_url)
    print("####################################################")
    print("####################################################")
    print("####################################################")
    print("sp_oauth", sp_oauth)
    print("auth_url", auth_url)
    print("code", code)
    print("####################################################")
    print("####################################################")
    print("####################################################")

    # Get access_token
    if code:
        print("Found Spotify auth code in Request URL! Trying to get valid access token...")
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']
    if access_token:
        print("Access token available!")
        sp = spotipy.Spotify(access_token)
    else:
        print("ERROR: Access token not available. Aborting login")
        quit()
    webbrowser.open(auth_url)

    response = {
        "action" : "User logged into spotify",
        "username" : sp.current_user()["display_name"],
        "code" : code,
        "access_token" : access_token,
        "auth_url" : auth_url
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
    
@app.route(('/apiv1/logout'), methods=['GET'])
def logout():
    webbrowser.open("https://accounts.spotify.com/en/logout")

    response = {
        "message" : "User logged out of spotify",
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route(('/apiv1/generateplaylist/'), methods=['POST'])
def generateplaylist():
    auth_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Set up exchange to place requests on. Worker will grab requests off exchange, and process them
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitMQHost))
    channel = connection.channel()

    # Exchange to send requests to worker
    channel.exchange_declare(exchange='toFirebaseSave',
                            exchange_type='direct')
    channel.queue_declare(queue='toFirebaseSave')

    data = request.get_json()
    access_token = data["access_token"]
    username = data["username"]

    # Get top 20 artists
    topArtistsJson = sp.current_user_top_artists(time_range='long_term')
    topArtists = []
    for artist in topArtistsJson['items']:
        topArtists.append(artist['uri'])
    
    playlist = []
    for artist in topArtists:
        # Select 2 songs from the top 50 songs for each artist
        artistTopTracks = sp.artist_top_tracks(artist)
        topTracks = []
        for track in artistTopTracks['tracks'][:50]:
            topTracks.append(track['name'])
        playlist.extend(random.sample(topTracks, 2))
    
    # Add playlist to queue, so it can be saved in firebase
    rbmqMessage = {
        "user" : username,
        "playlist" : playlist,
        "callback" : {
            "url": "http://localhost:5000",
            "data": {"some": "arbitrary", "data": "to be returned"}
        }
    }
    channel.basic_publish(exchange='', routing_key='toFirebaseSave', body=pickle.dumps(rbmqMessage))
    
    response = {
        "action" : "queued",
        "playlist" : playlist
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")



app.debug = True
# start flask app
app.run(host="0.0.0.0", port=5000)
    
