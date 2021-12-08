import spotipy
from spotipy import util

def getUserToken(username, scope, client_id, client_secret, redirect_uri):
    if username == None:
        print("User must be logged in to get token")
    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    return token