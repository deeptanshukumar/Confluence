# SpotifAI

**SpotifAI** is an interactive web application that generates playlists using OpenAI and Spotify API integration.

## Prerequisites

Ensure you have the following installed:

- Python (3.x recommended)
- Virtual Environment (`venv`)
- Flask and other dependencies (listed below)

## Project Setup

### 1. Setting Up the Virtual Environment

1. Navigate to your desired project directory:
   ```sh
   cd path/to/project
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows:**
     ```sh
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```sh
     source venv/bin/activate
     ```
4. Install Flask:
   ```sh
   pip install flask
   ```
5. Run the Flask server to verify installation:
   ```sh
   python ml.py
   ```
6. Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to check if the server is running.

## 2. Backend & Frontend Setup

### Installing Dependencies

Ensure the virtual environment is activated, then install the required dependencies:

```sh
pip install flask openai spotipy python-dotenv requests logging
```

### Configuring the `.env` File

1. **Spotify API Setup:**

   - Create a [Spotify Developer Account](https://developer.spotify.com/)
   - Navigate to **Dashboard → Your App → Settings**
   - Copy your `Client ID` and `Client Secret`
   - Set up a redirect URI as `http://localhost:5000/callback`

2. **AI API Setup:**

   - Sign up at [AIML API](https://api.aimlapi.com/)
   - Generate an API key from **API Settings**
   - Add the keys to your `.env` file:
     ```ini
     SPOTIPY_CLIENT_ID=your_spotify_client_id
     SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
     AI_BASE_URL=https://api.aimlapi.com
     AI_API_KEY=YOUR_API_KEY
     ```

## 3. Project Structure

Follow this directory structure while working on the project:

```
SPOTIFAI/
│-- venv/
│-- static/           # Frontend assets (CSS, JS, images)
│-- templates/        # HTML templates
│-- ml.py             # Main Flask backend
│-- .env              # Environment variables
│-- requirements.txt  # List of dependencies
│-- README.md         # Project documentation
```

## 4. Running the Application

1. Ensure the virtual environment is activated.
2. Run the application:
   ```sh
   python ml.py
   ```
3. Copy the URL displayed in the terminal (`http://127.0.0.1:5000/`).
4. Open the URL in your browser and start using **SPOTIFAI**!

---

### Notes

- Always activate the virtual environment before running the app.
- If you install new dependencies, update `requirements.txt` using:
  ```sh
  pip freeze > requirements.txt
  ```

Enjoy your playlist creation experience with **SPOTIFAI**! 🎵✨

## Credits

Contributors:

- [Sai Rishi Gangarapu](https://github.com/sairishigangarapu)
- [Ponakala Yathish](https://github.com/Ponakala-Yathish)
- [Deeptanshu Kumar](https://github.com/deeptanshukumar)
- [Sharath Doddihal](https://github.com/venkamita)

