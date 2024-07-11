Overview
This project is a Flask-based web application for a music recommendation system. It utilizes machine learning models to predict songs based on user-selected moods and recommends similar tracks using cosine similarity. The application also integrates with the Spotify API to fetch song details and generate playlists.

<img width="1431" alt="image" src="https://github.com/user-attachments/assets/ab12d0b0-1317-487e-ae38-e654e5862a1f">


Features
Mood-based Song Recommendations: Users can select a mood, and the application will suggest songs that match the mood using a pre-trained Random Forest model.
Track-based Recommendations: Users can input a specific song ID, and the application will recommend similar tracks based on acoustic features.
Spotify Integration: Fetches detailed information about tracks using the Spotify API.
Interactive UI: Simple and interactive user interface built using Flask and rendered with Jinja2 templates.
Prerequisites
Python 3.x
Flask
Joblib
Pandas
Numpy
Requests
Scikit-learn
Setup and Installation
Clone the Repository:

sh
Copy code
git clone <repository_url>
cd <repository_directory>
Install Dependencies:

sh
Copy code
pip install -r requirements.txt
Place the Pre-trained Models:

Ensure you have the following files in the root directory of your project:

random_forest_music_model.joblib
label_encoder.joblib
Spotify API Credentials:

Replace the CLIENT_ID and CLIENT_SECRET in the code with your Spotify API credentials.

Dataset:

Ensure the updated_data.csv file is in the root directory of your project.

Running the Application
Start the Flask Server:

sh
Copy code
python app.py
Access the Application:

Open your web browser and navigate to http://127.0.0.1:5000.

API Endpoints
Home Page:

Endpoint: /
Methods: GET, POST
Description: Displays the home page where users can select a mood and get song recommendations.
Recommend Similar Tracks:

Endpoint: /recommend

Methods: POST

Description: Accepts a JSON object with a track_id and returns a list of similar tracks.

Sample Request:

json
Copy code
{
    "track_id": "3n3Ppam7vgaVa1iaRUc9Lp"
}
Code Explanation
app.py:

This is the main application file which includes:

Importing necessary libraries.
Loading pre-trained models and dataset.
Defining Flask routes for the home page and recommendation functionality.
Functions to handle Spotify API authentication and data fetching.
Functions to compute recommendations based on user input.
Templates:

index.html: The HTML template for rendering the home page with mood selection and song recommendations.
Spotify API Integration
Authentication:

The get_token function uses Spotify's Client Credentials Flow to authenticate and obtain an access token.

Fetching Track Details:

Track details are fetched using the Spotify API by making a GET request with the track IDs.

Future Improvements
Add user authentication and personalized recommendations.
Enhance the recommendation algorithm using additional features and models.
Integrate with more music streaming services.
