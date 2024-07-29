import requests
from django.utils import timezone
from ..exceptions import InvalidSpotifyToken, SpotifyResponseException
from ..services import get_spotify_token
from ..serializers import SearchSerializer, AlbumSerializer
from ..models import Album, Search
from .album import get_albums, save_album

# MAX_SEARCH_STORAGE_TIME = timedelta(minutes=5)
SEARCH_HOURS_INTERVAL = 8

def get_current_search_hours_interval():
    now = timezone.now()
    # print('----now        :     ', now)
    hour = (now.hour // SEARCH_HOURS_INTERVAL) * SEARCH_HOURS_INTERVAL
    current_interval = now.replace(hour=hour, minute=1, second=0, microsecond=0)
    return current_interval

# def get_current_search_hour_interval():
#     now = timezone.now()
#     # print('----now        :     ', now)
#     if now.minute <= 1 and now.second < 30:
#         current_interval = (now - timezone.timedelta(hours=1)).replace(minute=1, second=30, microsecond=0)
#     else:
#         current_interval = now.replace(minute=1, second=30, microsecond=0)
#     return current_interval

def is_in_valid_search_interval(last_update):
    current_interval = get_current_search_hours_interval()
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

def old_searches(days=1, detailed=False, clean=False):
        now = timezone.now()
        limit_date = now - timezone.timedelta(days=days)
        searches_to_delete = Search.objects.filter(updated_at__lte=limit_date)

        count = searches_to_delete.count()
        response_data = {
            'days': days,
            'now': now,
            'limit': limit_date,
            'count': count
        }

        if detailed:
            s_s = SearchSerializer(searches_to_delete, many=True)
            response_data['searches'] = [s['q'] for s in s_s.data]

        if clean:
            deleted_count, _ = searches_to_delete.delete()
            response_data['deleted_count'] = deleted_count

        return response_data
