import requests
from ..exceptions import InvalidSpotifyToken, SpotifyResponseException
from ..services import get_spotify_token

def search_albums(q):
    try:
        access_token = get_spotify_token()
    except Exception as e:
        raise e

    search_url = f'https://api.spotify.com/v1/search?q={q}&type=album'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise InvalidSpotifyToken
    else:
        raise SpotifyResponseException(response)
    