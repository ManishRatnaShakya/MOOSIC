from flask import Flask, jsonify, redirect, request, render_template, url_for
import joblib
import pandas as pd
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the model and the label encoder
model = joblib.load('random_forest_music_model.joblib')
label_encoder = joblib.load('label_encoder.joblib')
# Load the pre-trained model
# nn_model = joblib.load('k_nearest_music_model.joblib')

# xbg_model = joblib.load('xgb_music_recommendation_model.joblib')
# Spotify API credentials
CLIENT_ID = '3dc7fa2ebec4490d9ddd167ea62d7917'
CLIENT_SECRET = '12cd6003a455428eb4e40c7e278d1e4d'
AUTH_URL = 'https://accounts.spotify.com/api/token'

# Load the dataset
data = pd.read_csv('updated_data.csv')
feature_columns = ['valence', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness',
                   'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']



@app.route('/', methods=['GET', 'POST'])
def index():
    token = get_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
 
    selected_mood = None

    if request.method == 'POST':
        selected_mood = request.form.get('mood')
        mood_index = label_encoder.transform([selected_mood])[0]
        predictions = model.predict(data[feature_columns])
        mood_songs = data[predictions == mood_index]
        songs_sample = mood_songs[['artists', 'name', 'id']].sample(n=20)
        songs_list = songs_sample.to_dict(orient='records')
        
        ids_list = [song['id'] for song in songs_list]
        ids = ','.join(ids_list)
        response = requests.get(f"https://api.spotify.com/v1/tracks?ids={ids}", headers=headers)
        playlist = response.json()  
        tracks = playlist['tracks']
        return render_template('index.html', songs=tracks, moods=label_encoder.classes_, selected_mood = selected_mood )
    return render_template('index.html', moods=label_encoder.classes_)

@app.route('/recommend', methods=['GET','POST'])
def recommend():
    user_input = request.json
    song_id = user_input['track_id']
    # Assuming 'song_id' is a column in your dataset
    selected_song_features = data.loc[data['id'] == song_id, ['acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'tempo']]

    # Calculate cosine similarity
    similarities = cosine_similarity(data[['acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'tempo']], selected_song_features).flatten()

    # Add similarity scores to the DataFrame
    data['similarity'] = similarities

    # Get top 5 similar songs
    recommendations = data.sort_values(by='similarity', ascending=False).head(20)

    # Exclude the selected song from the recommendations
    recommendations = recommendations[recommendations['id'] != song_id]
    recommended_ids = recommendations['id'].tolist()
    print(recommended_ids)
    
    ids = ','.join(recommended_ids)
    token = get_token()
    headers = {
            'Authorization': f'Bearer {token}'
        }
    response = requests.get(f"https://api.spotify.com/v1/tracks?ids={ids}", headers=headers)
    playlist = response.json()  
    tracks = []
    tracks = playlist['tracks']
    return jsonify(tracks)

# def recommend():
#     if request.method == 'POST':
#         # Get user input
#         token = get_token()
#         headers = {
#             'Authorization': f'Bearer {token}'
#         }
#         user_input = request.json
#         track_id = user_input['track_id']

#         # Extract features for the selected track
#         track_features = data[data['id'] == track_id][[
#             'acousticness', 'danceability', 'energy', 'instrumentalness',
#             'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence'
#         ]].iloc[0].values.reshape(1, -1)

#         # Use the model to find nearest neighbors
#         distances, indices = nn_model.kneighbors(track_features)

#         # Retrieve recommended tracks
#         recommended_tracks = data.iloc[indices[0]][['name', 'artists', 'id']].to_dict(orient='records')
        
#         ids_list = [song['id'] for song in recommended_tracks]
#         ids = ','.join(ids_list)
#         response = requests.get(f"https://api.spotify.com/v1/tracks?ids={ids}", headers=headers)
#         playlist = response.json()  
#         tracks = playlist['tracks']
#         return jsonify(tracks)

# Function to get token using Client Credentials Flow
def get_token():
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    auth_response_data = auth_response.json()
    access_token = auth_response_data.get('access_token')
    return access_token



# if __name__ == '__main__':
#     app.run(debug=True)