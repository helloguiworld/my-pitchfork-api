import requests
from ..exceptions import InvalidSpotifyToken
from ..services import get_spotify_token

def get_album(id):
    try:
        access_token = get_spotify_token()
    except Exception as e:
        raise e

    search_url = f'https://api.spotify.com/v1/albums/{id}'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise InvalidSpotifyToken
    else:
        raise Exception(f"Failed to search albums: {response.status_code}, {response.text}")
    