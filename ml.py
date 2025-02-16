from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from openai import OpenAI
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import logging
import os
import spotipy

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'your_redircting_url)

AI_BASE_URL = os.getenv('AI_BASE_URL', 'https://api.aimlapi.com')
AI_API_KEY = os.getenv('AI_API_KEY')

SCOPE = 'playlist-modify-public playlist-modify-private user-read-private user-read-email'

system_prompt = """
Create a playlist and return in format:
1. Song1 by Artist1
2. Song2 by Artist1 or Artist2
"""

api = OpenAI(api_key=AI_API_KEY, base_url=AI_BASE_URL)

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE
    )

@app.route('/')
def index():
    if not session.get('token_info'):
        return redirect(url_for('login_page'))
    
    try:
        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        user_info = sp.current_user()
        spotify_profile_url = user_info['external_urls']['spotify']
        
        return render_template('index.html', 
                             logged_in=True,
                             profile_url=spotify_profile_url)
    except Exception as e:
        logging.error(f"Error accessing Spotify: {e}")
        session.clear()
        return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login/spotify')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('filters'))  

@app.route('/logout')
def logout():
    session.clear()
    
    spotify_logout_url = 'https://accounts.spotify.com/en/logout'
    app_login_url = 'your_redirectning_url_unitl_the_port/login'
    
    return """
    <script>
        fetch('{spotify_logout_url}', {{
            method: 'POST',
            credentials: 'include'
        }}).finally(() => {{
            window.location.href = '{app_login_url}';
        }});
    </script>
    """.format(spotify_logout_url=spotify_logout_url, app_login_url=app_login_url)

@app.route('/filters')
def filters():
    if not session.get('token_info'):
        return redirect(url_for('login_page'))
    
    try:
        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        user_info = sp.current_user()
        spotify_profile_url = user_info['external_urls']['spotify']
        
        return render_template('filters.html', 
                             logged_in=True,
                             profile_url=spotify_profile_url)
    except Exception as e:
        logging.error(f"Error accessing Spotify: {e}")
        session.clear()
        return redirect(url_for('login_page'))

@app.route('/get_playlist', methods=['POST'])
def get_playlist():
    if not session.get('token_info'):
        return jsonify({"error": "Not logged in"}), 401

    try:
        data = request.json
        user_input = data.get("user_input")

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        formatted_input = f"Mood: {user_input['mood']}, Genres: {', '.join(user_input['genres'])}"
        if user_input['artists']:
            formatted_input += f", Artists: {', '.join(user_input['artists'])}"
        formatted_input += f", Number of Songs: {user_input['numSongs']}"

        logging.debug("Calling OpenAI API...")
        completion = api.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_input},
            ],
            temperature=0.7,
            max_tokens=256,
        )

        recommendations = completion.choices[0].message.content
        logging.debug(f"AI Recommendations: {recommendations}")

        if not recommendations.strip():
            return jsonify({"error": "No songs recommended by AI"}), 400

        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        user_id = sp.current_user()['id']

        playlist_name = f"AI Generated Playlist - {user_input['mood']}"
        logging.debug(f"Creating playlist: {playlist_name}")
        playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
        playlist_id = playlist['id']
        songs = recommendations.split('\n')
        track_uris = []

        for song in songs:
            if song.strip():
                parts = song.split(' by ')
                if len(parts) == 2:
                    track_name = parts[0].split('. ')[-1].strip()
                    artist_name = parts[1].strip()
                    query = f"track:{track_name} artist:{artist_name}"
                    logging.debug(f"Searching Spotify for: {query}")
                    result = sp.search(query, type='track', limit=1)

                    if result['tracks']['items']:
                        track_uris.append(result['tracks']['items'][0]['uri'])

        if track_uris:
            logging.debug(f"Adding {len(track_uris)} tracks to the playlist")
            sp.playlist_add_items(playlist_id, track_uris)
        else:
            return jsonify({"error": "No tracks found on Spotify"}), 400

        embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
        return jsonify({"embed_url": embed_url})

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
