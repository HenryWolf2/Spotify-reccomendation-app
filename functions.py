import base64
import os
import requests
import spotipy
from dotenv import load_dotenv
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
ID = os.getenv('CLIENT_ID')
SECRET = os.getenv('CLIENT_SECRET')

credentials = ID + ":" + SECRET
credentials_base = base64.b64encode(credentials.encode())

spotify_access_url = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': f'Basic {credentials_base.decode()}'
}
data = {
    'grant_type': 'client_credentials'
}

request = requests.post(spotify_access_url, headers=headers, data=data)

# Get the access token
if request.status_code == 200:
    json_response = request.json()
    spotify_access_token = json_response['access_token']

spotify = spotipy.Spotify(auth=spotify_access_token)


def trending_track_data(playlist_id, access_token):
    # Get information about tracks
    tracks = spotify.playlist_items(playlist_id, fields='items(track(id, name, album(id, name), artists))')
    songs = []
    for info in tracks['items']:
        print(info)
        track = info['track']
        name = track['name']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        album_name = track['album']['name']
        album_id = track['album']['id']
        track_id = track['id']
        try:
            if track_id != 'Not available':
                info = spotify.track(track_id)
                audio = spotify.audio_features(track_id)[0]
            else:
                audio = None
                info = None
            if info:
                popularity = info['popularity']
            else:
                popularity = None
        except:
            popularity = None

        track_dict = {
            'Track Name': name,
            'Artists': artists,
            'Album Name': album_name,
            'Album ID': album_id,
            'Track ID': track_id,
            'Popularity': popularity,
        }
        songs.append(track_dict)
    dataframe = pd.DataFrame(songs)
    return dataframe




data = trending_track_data('6Nn8Ai1bkouFuCSXbtwlJf', spotify_access_token)
print(data)
