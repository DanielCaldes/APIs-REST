from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
import requests
from base64 import b64encode
from typing import List, Optional
from dotenv import load_dotenv

# COMANDO: uvicorn "main:app" --reload
# URL SWAGGER: http://localhost:8000/docs

app = FastAPI()

load_dotenv()

#Define constants
DATABASE = os.path.join("music_app.db")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_db_connection():
    return sqlite3.connect(DATABASE)   

#Databases
def init_users_db():
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE
            )
            """
        )

def init_favourite_artist_db():
    with get_db_connection() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS favourite_artists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                artist_id TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE (user_id, artist_id)
            )
            """
        )

def init_favourite_tracks_db():
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS favourite_tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                track_id TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE (user_id, track_id)
            )
            """
        )        

init_users_db()
init_favourite_artist_db()
init_favourite_tracks_db()

# --------------------------------
# Users API

# Calls
# POST      http://127.0.0.1:8000/api/users/             {"username":"nombre"}
# GET       http://127.0.0.1:8000/api/users/
# PUT       http://127.0.0.1:8000/api/users/<user_id>    {"username":"nombre"}
# DELETE    http://127.0.0.1:8000/api/users/<user_id>

# Define pydantic class to valid data
class User(BaseModel):
    username : str

# Define the operations for the API users
@app.post("/api/users/", status_code=201, tags=["Users"])
def create_user(user : User):
    """
    Create a new user.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users(username) VALUES (?)", (user.username,)
            )
            conn.commit()
            return {"id":cursor.lastrowid}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.get("/api/users/", response_model=List[User], tags=["Users"])
def get_users():
    """
    Get all users
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT id, username FROM users"
            )
            users = [{"id":user[0], "username":user[1]} for user in cursor.fetchall()]
            return users
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An unexpected error occurred: {str(e)}")

@app.put('/api/users/{user_id}', tags=["Users"])
def update_user(user_id : int, user : User):
    """
    Update the user with the provided ID
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "UPDATE users SET username = (?) WHERE id = (?)", (user.username,user_id)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"No user with id {user_id} found")
            return {"message" : "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.delete('/api/users/{user_id}', tags=["Users"])
def delete_user(user_id : int):
    """
    Delete a user by their ID
    """
    try:
        with get_db_connection() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.execute(
                "DELETE FROM users WHERE id = (?)", (user_id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
            return {"message":f"User with id {user_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# --------------------------------
# Store user mussic preferences

# Calls
# POST      http://127.0.0.1:8000/api/users/<user_id>/favourites/artists/    {"spotify_artist_id":artist_id}
# DELETE    http://127.0.0.1:8000/api/users/<user_id>/favourites/artists/    {"spotify_artist_id":artist_id}

# POST      http://127.0.0.1:8000/api/users/<user_id>/favourites/tracks/     {"spotify_track_id":track_id}
# DELETE    http://127.0.0.1:8000/api/users/<user_id>/favourites/tracks/     {"spotify_track_id":track_id}

#For testing -> Artist_id(Pitbull) : 0TnOYISbd1XYRBk9myaseg  Track_id(Cut To The Feeling) : 11dFghVXANMlKmJXsNCbNl

# Define pydantic class to valid data
class Favourite_Artist(BaseModel):
    spotify_artist_id : str

class Favourite_Track(BaseModel):
    spotify_track_id : str

@app.post('/api/users/{user_id}/favourites/artists/', tags=["Favourites"])
def add_favourite_artist(user_id:int, favourite_artist : Favourite_Artist):
    """
    Add a favorite artist for a user
    """
    try:
        with get_db_connection() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute(
                """
                    INSERT INTO favourite_artists (user_id, artist_id)
                    VALUES (?, ?)
                """
                , (
                    user_id,
                    favourite_artist.spotify_artist_id
                )
            )
            conn.commit()
        rows_affected = conn.total_changes
        if rows_affected > 0:
            return {"message": "Insert successful!"}
        else:
            raise HTTPException(status_code=500, detail="Insert failed, no rows affected!")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")

@app.delete('/api/users/{user_id}/favourites/artists/', tags=["Favourites"])
def remove_favourite_artist(user_id:int, favourite_artist : Favourite_Artist):
    """
    Remove an artist from a user's favorites
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM favourite_artists WHERE user_id = (?) AND artist_id = (?)",
                ( user_id, favourite_artist.spotify_artist_id )
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Remove failed, check user_id and artist_id")
            return {'message' : 'Artist preference removed!'}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")

@app.post('/api/users/{user_id}/favourites/tracks/', tags=["Favourites"])
def add_favourite_track(user_id:int, favourite_track :Favourite_Track):
    """
    Add a track to a user's favorites
    """
    try:
        with get_db_connection() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute(
                """
                    INSERT INTO favourite_tracks (user_id, track_id)
                    VALUES (?, ?)
                """
                , (
                    user_id,
                    favourite_track.spotify_track_id
                )
            )
            conn.commit()
        rows_affected = conn.total_changes
        if rows_affected > 0:
            return {"message": "Insert successful!"}
        else:
            raise HTTPException(status_code=500, detail="Insert failed, no rows affected!")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")

@app.delete('/api/users/{user_id}/favourites/tracks/', tags=["Favourites"])
def remove_favourite_track(user_id:int, favourite_track :Favourite_Track):
    """
    Remove a song from a user's favorites
    """
    try:
        with get_db_connection() as conn:
                cursor = conn.execute(
                    "DELETE FROM favourite_tracks WHERE user_id = (?) AND track_id = (?)",
                    ( user_id, favourite_track.spotify_track_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Remove failed, check user_id and track_id")
                return {'message' : 'Track preference removed!'}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")

# --------------------------------
# Connect to Spotify

# Calls
# GET  http://127.0.0.1:8000/api/spotify/artists/<artist_name>
# GET  http://127.0.0.1:8000/api/users/<user_id>/favourites/artists/<user_id>

# GET  http://127.0.0.1:8000/api/spotify/tracks/<track_name>
# GET  http://127.0.0.1:8000/api/spotify/tracks/<track_name>/<artist_name>
# GET  http://127.0.0.1:8000/api/users/<user_id>favourites/tracks/<user_id>

def get_spotify_token():
    #Generate the necessary data to make the request to Spotify
    url = "https://accounts.spotify.com/api/token"
    credentials = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode('utf-8')).decode('utf-8')
    headers = { "Authorization": f"Basic {credentials}" }
    data = { "grant_type": "client_credentials" }

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        print("Error obtaining the token:", response.status_code)
        return None

access_token = get_spotify_token()

def spotify_request(endpoint: str, params: Optional[dict] = None):
    """Make a request to the Spotify API and handle the access token."""
    url = f"https://api.spotify.com/v1/{endpoint}"
    
    global access_token
    headers = { 'Authorization': f'Bearer {access_token}' }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("The token has expired, obtaining a new one...")
        access_token = get_spotify_token()
        headers = { 'Authorization': f'Bearer {access_token}' }
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error in the request after refreshing the token: {response.status_code}, {response.text}")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error in the request: {response.status_code}, {response.text}")


class Artist(BaseModel):
    name: str
    id: str
    uri: str

class Track(BaseModel):
    name: str            
    id: str              
    uri: str             
    artists: List[Artist]

# Artists
@app.get('/api/spotify/artists/{artist_name}', response_model=Artist, tags=["Spotify"])
def search_artist_by_name(artist_name : str):
    """
    Get the Spotify data for the artist
    """

    params = {
        'q': artist_name,
        'type': 'artist',
        'limit': 1
    }
    
    data = spotify_request("search",params)
    
    if not data or 'artists' not in data or 'items' not in data['artists'] or not data['artists']['items']:
        raise HTTPException(status_code=404, detail="No artist was found with that name.")
    
    artist = data['artists']['items'][0]
    return Artist(
        name = artist['name'],
        id = artist['id'],
        uri = artist['uri']
    )

def search_artist_by_id(spotify_artist_id : str):
    artist = spotify_request(f"artists/{spotify_artist_id}")
    
    if artist:
        return Artist(
            id=artist['id'],
            name=artist['name'],
            uri=artist['uri']
        )
    else:
        raise HTTPException(status_code=404, detail="Artist not found.")

@app.get('/api/users/{user_id}/favourites/artists/', response_model=List[Artist], tags=["Favourites"])
def get_favourites_artists(user_id : int):
    """
    Get the favorite artists of a user
    """
    favourites_artists = []
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT artist_id FROM favourite_artists WHERE user_id = ?",
                (user_id,)
            )
            favourites_artists_ids = [row[0] for row in cursor.fetchall()]
        
        for artist_id in favourites_artists_ids:
            favourites_artists.append(search_artist_by_id(artist_id))
        return favourites_artists
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Tracks
def search_track_by_id(spotify_track_id : str):
    track_data = spotify_request(f"tracks/{spotify_track_id}")
    if track_data:
        artists = [Artist(
            name=artist['name'],
            id=artist['id'],
            uri=artist['uri']
        ) for artist in track_data['artists']]
        
        track = Track(
            name=track_data['name'],
            id=track_data['id'],
            uri=track_data['uri'],
            artists=artists
        )
        return track
    else:
        return HTTPException(status_code=404, detail="Track not found.")

@app.get('/api/spotify/tracks/{track_name}', tags=["Spotify"])
@app.get('/api/spotify/tracks/{track_name}/{artist_name}', response_model=Track, tags=["Spotify"])
def search_track_by_name(track_name : str, artist_name : Optional[str] = ""):
    """
    Search for tracks on Spotify by track name and optional artist name.
    If no artist name is provided, it returns the top tracks sorted by popularity.
    """
    
    if artist_name:
        query = f"track:{track_name} artist:{artist_name}"
        limit = 1
    else:
        query = f"track:{track_name}"
        limit = 50
    params = {
        'q': query,
        'type': 'track',
        'limit': limit
    }
    
    data = spotify_request("search", params)
    
    if data['tracks']['items']:
        if limit == 1:
            track = data['tracks']['items'][0]
            return Track(
                name=track['name'],
                id=track['id'],
                uri=track['uri'],
                artists=[Artist(
                    name=artist['name'],
                    id=artist['id'],
                    uri=artist['uri']) for artist in track['artists']])
        else:
            artists_dict = {}
            tracks = data['tracks']['items']
            tracks_sorted = sorted(tracks, key=lambda x: x['popularity'], reverse=True)
            for track in tracks_sorted:
                for artist in track['artists']:
                    artist_name = artist['name']
                    track_popularity = track['popularity']
                    if artist_name not in artists_dict or track_popularity > artists_dict[artist_name]['track_popularity']:
                        artists_dict[artist_name] = {
                            'artist_name': artist_name,
                            'track_popularity': track_popularity
                            }
            return [{"artist_name": artist['artist_name'], "track_popularity": artist['track_popularity']}
                    for artist in artists_dict.values()]
    else:
        raise HTTPException(status_code=404, detail="No track found with the given name.")

@app.get('/api/users/{user_id}/favourites/tracks/', response_model=List[Track], tags=["Favourites"])
def get_favourites_tracks(user_id : int):
    """
    Get the favorite tracks of a user
    """
    favourites_tracks = []
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT track_id FROM favourite_tracks WHERE user_id = ?",
                (user_id,)
            )
            favourites_tracks_ids = [row[0] for row in cursor.fetchall()]
        
        for track_id in favourites_tracks_ids:
            favourites_tracks.append(search_track_by_id(track_id))
        return favourites_tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
