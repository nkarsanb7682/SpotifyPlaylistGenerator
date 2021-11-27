import pandas as pd
import json

# Read in all data
for value in range(0, 1000000, 1000):
    print("Playlists {}-{}".format(value, value + 999))
    df = pd.DataFrame()
    with open('../spotify_million_playlist_dataset/data/mpd.slice.{}-{}.json'.format(value, value + 999), 'r') as f:
        file = f.read()

    data = json.loads(file)
    playlists = data['playlists']
    for playlistNum in range(len(playlists)):
        track = pd.json_normalize(playlists[playlistNum], 'tracks', errors='ignore')
        track["playlist_name"] = playlists[playlistNum]["name"]
        df = df.append(track)
    df.to_pickle("../DataFrames/pickledPLaylist_{}-{}".format(value, value + 999))

