import requests
from django.utils import timezone
from datetime import timedelta
from ..exceptions import InvalidSpotifyToken, SpotifyResponseException
from ..services import get_spotify_token
from ..serializers import SearchSerializer, AlbumSerializer
from ..models import Album, Search
from .album import get_albums, save_album

# MAX_SEARCH_STORAGE_TIME = timedelta(minutes=5)
SEARCH_MINUTES_INTERVAL = 15

def get_current_search_interval():
    now = timezone.now()
    minutes = (now.minute // SEARCH_MINUTES_INTERVAL) * SEARCH_MINUTES_INTERVAL + 1
    current_interval = now.replace(minute=minutes, second=30, microsecond=0)
    return current_interval

def is_in_valid_search_interval(last_update):
    current_interval = get_current_search_interval()
    print('----last update:     ', last_update)
    print('----current interval:', current_interval)
    return current_interval < last_update

def save_search(q, albums):
    search, created = Search.objects.update_or_create(q=q,)
    search.albums.set(albums)
    search.save()
    return search

def search_albums(q):
    try:
        search = Search.objects.get(q=q)
        if is_in_valid_search_interval(search.updated_at):
            print(f'GOT STORED SEARCH {q}')
            search_serializer = SearchSerializer(search)
            return search_serializer.data['albums']
    except Search.DoesNotExist:
        print(f'NEW SEARCH {q}')
        pass

    try:
        access_token = get_spotify_token()
    except Exception as e:
        raise e
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    search_url = f'https://api.spotify.com/v1/search?q={q}&type=album&limit=10'
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        search_results = response.json()
        
        album_ids = [album['id'] for album in search_results['albums']['items']]
        albums_datas = get_albums(album_ids)
        
        saved_albums = []
        for album in albums_datas:
            saved_album = save_album(album)
            saved_albums.append(saved_album)
            
        saved_search = save_search(q, saved_albums)
        print(f'SAVED SEARCH {q}')
        
        search_serializer = SearchSerializer(saved_search)
        return search_serializer.data['albums']
    elif response.status_code == 401:
        raise InvalidSpotifyToken
    else:
        raise SpotifyResponseException(response)
    