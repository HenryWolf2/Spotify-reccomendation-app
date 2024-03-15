import base64
import os
import requests
import spotipy
from dotenv import load_dotenv
import pandas as pd
from sklearn.model_selection import train_test_split
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
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
            'Acousticness': audio['acousticness'] if audio else None,
            'Instrumentalness': audio['instrumentalness'] if audio else None,
            'Liveness': audio['liveness'] if audio else None,
            'Valence': audio['valence'] if audio else None,
            'Danceability': audio['danceability'] if audio else None,
            'Energy': audio['energy'] if audio else None,
            'Tempo': audio['tempo'] if audio else None,
            'Key': audio['key'] if audio else None,
            'Loudness': audio['loudness'] if audio else None,
            'Mode': audio['mode'] if audio else None,
            'Speechiness': audio['speechiness'] if audio else None,
        }
        songs.append(track_dict)
    dataframe = pd.DataFrame(songs)
    return dataframe

def feature_based(input_song_name, playlist_df, scaled_features, num_recommendations=3):
    # A function to get recommendations based on music features.
    # It takes the inputted song name and returns 3 similar songs.
    if input_song_name not in playlist_df['Track Name'].values:
        print( input_song_name + " not found in the playlist.")
    input_song_index = playlist_df[playlist_df['Track Name'] == input_song_name].index[0]
    similarity_scores = cosine_similarity([scaled_features[input_song_index]], scaled_features)
    similar_song_indices = similarity_scores.argsort()[0][::-1][1:num_recommendations + 1]
    feature_based_recommendations = playlist_df.iloc[similar_song_indices][['Track Name', 'Artists', 'Album Name', 'Popularity']]
    return feature_based_recommendations