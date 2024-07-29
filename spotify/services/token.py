import os
import requests
from ..exceptions import InvalidSpotifyToken, SpotifyResponseException

def get_spotify_token_infos():
    token_url = "https://accounts.spotify.com/api/token"
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to obtain token: {response.status_code}, {response.text}")


def get_new_spotify_token():
    try:
        token_infos = get_spotify_token_infos()
        return token_infos['access_token']
    except Exception as e:
        raise e


def get_spotify_token():
    try:
        access_token = os.environ['SPOTIFY_ACCESS_TOKEN']
    except KeyError:
        try:
            access_token = setup_spotify_token()
        except Exception as e:
            raise e
    
    return access_token


def setup_spotify_token():
    try:
        token_infos = get_spotify_token_infos()
        
        access_token = token_infos['access_token']
        os.environ['SPOTIFY_ACCESS_TOKEN'] = access_token
        
        return access_token
    except Exception as e:
        print(f"Error obtaining Spotify token: {e}")
        raise e


def execute_spotify_with_token_retry(action, *args, **kwargs):
    try:
        return action(*args, **kwargs)
    except InvalidSpotifyToken:
        try:
            setup_spotify_token()
            return action(*args, **kwargs)
        except Exception as e:
            raise e
