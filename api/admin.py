from django.contrib import admin
from .models import Share, Account, SearchClick, AlbumClick, Review, TrackScore

admin.site.register(Share)
admin.site.register(Account)
admin.site.register(SearchClick)
admin.site.register(AlbumClick)
admin.site.register(Review)
admin.site.register(TrackScore)
