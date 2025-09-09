import requests
from django.utils import timezone
from django.db.models import Count
from django.db.models.deletion import ProtectedError
from datetime import timedelta
from ..exceptions import InvalidSpotifyToken, SpotifyResponseException
from . import get_spotify_token
from ..models import Album, Track
from ..serializers import AlbumCompleteSerializer

MAX_ALBUM_STORAGE_TIME = timedelta(hours=12)

def clean_album(album):
    return {
        'id': album['id'],
        'name': album['name'],
        'type': album['album_type'],
        'cover': album['images'][0]['url'],
        'artists': [artist['name'] for artist in album['artists']],
        'date': album['release_date'],
        'tracks_count': album['total_tracks'],
        'total_tracks': album['total_tracks'],
        'tracks': [{
            'id': track['id'],
            'name': track['name'],
            'artists': [artist['name'] for artist in track['artists']],
            'explicit': track['explicit'],
            'number': index+1,
        } for index, track in enumerate(album['tracks']['items'])],
    }

def save_album(album_data):
    album = clean_album(album_data)
    tracks = album.pop('tracks')
    
    explicit = any(track['explicit'] for track in tracks)
    album['explicit'] = explicit
    
    saved_album, _ = Album.objects.update_or_create(
        id=album['id'],
        defaults={
            'id': album['id'],
            'data': album,
        }
    )
    
    for track in tracks:
        Track.objects.update_or_create(
            id=track['id'],
            defaults={
                'id': track['id'],
                'album': saved_album,
                'data': track,
            }
        )
    
    return saved_album

def get_album(id):
    try:
        album = Album.objects.get(id=id)
        print('----last update:', album.updated_at)
        print('----time now:   ', timezone.now())
        if timezone.now() - album.updated_at < MAX_ALBUM_STORAGE_TIME:
            print(f'GOT STORED ALBUM {album}')
            album_serializer = AlbumCompleteSerializer(album)
            return album_serializer.data['data']
    except Album.DoesNotExist:
        print(f'NEW ALBUM {id}')
        pass

    try:
        access_token = get_spotify_token()
    except Exception as e:
        raise e

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    album_url = f'https://api.spotify.com/v1/albums/{id}'
    response = requests.get(album_url, headers=headers)
    
    if response.status_code == 200:
        album_result = response.json()
        saved_album = save_album(album_result)
        print('SAVED ALBUM')
        album_serializer = AlbumCompleteSerializer(saved_album)
        return album_serializer.data['data']
    elif response.status_code == 401:
        raise InvalidSpotifyToken
    else:
        raise SpotifyResponseException(response)

def get_albums(ids):
    try:
        access_token = get_spotify_token()
    except Exception as e:
        raise e

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    ids_str = ','.join(ids)
    albums_url = f'https://api.spotify.com/v1/albums?ids={ids_str}'
    response = requests.get(albums_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['albums']
    elif response.status_code == 401:
        raise InvalidSpotifyToken
    else:
        raise SpotifyResponseException(response)

def old_albums(days=1, detailed=False, clean=False):
        now = timezone.now()
        limit_date = now - timezone.timedelta(days=days)
        albums_to_delete = (Album.objects
            .annotate(reviews_count=Count('reviews'))
            .filter(updated_at__lte=limit_date, reviews_count__exact=0)
        )

        count = albums_to_delete.count()
        response_data = {
            'days': days,
            'now': now,
            'limit': limit_date,
            'count': count,
        }

        if detailed:
            response_data['albums'] = [a.name for a in albums_to_delete]

        if clean:
            deleted_count, _ = albums_to_delete.delete()
            response_data['deleted_count'] = deleted_count
    
        return response_data

def old_albums2(days=1, detailed=False, clean=False):
    now = timezone.now()
    limit_date = now - timezone.timedelta(days=days)
    albums_to_delete = (Album.objects
        .annotate(reviews_count=Count('reviews'))
        .filter(updated_at__lte=limit_date, reviews_count__exact=0)
    )

    count = albums_to_delete.count()
    response_data = {
        'days': days,
        'now': now,
        'limit': limit_date,
        'count': count,
    }

    if detailed:
        response_data['albums'] = [a.name for a in albums_to_delete]

    if clean:
        deleted_total = 0
        for album in albums_to_delete:
            try:
                deleted_count, _ = album.delete()
                deleted_total += deleted_count
            except ProtectedError:
                # Ignora álbuns que não podem ser deletados e continua
                continue
        response_data['deleted_count'] = deleted_total

    return response_data