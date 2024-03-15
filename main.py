from functions import trending_track_data, feature_based ,spotify_access_token
from sklearn.preprocessing import MinMaxScaler

data = trending_track_data('6Nn8Ai1bkouFuCSXbtwlJf', spotify_access_token)
scaler = MinMaxScaler()
music_features = data[['Danceability', 'Energy', 'Key',
                           'Loudness', 'Mode', 'Speechiness', 'Acousticness',
                           'Instrumentalness', 'Liveness', 'Valence', 'Tempo']].values
music_features_scaled = scaler.fit_transform(music_features)
# recommendations = feature_based('Giant Tortoise', data, music_features_scaled)