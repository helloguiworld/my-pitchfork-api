from django.contrib import admin
from .models import ShareClick, Account, SearchClick, AlbumClick, Review, TrackScore, Follow

admin.site.register(Account)
admin.site.register(Follow)

admin.site.register(Review)
admin.site.register(TrackScore)

admin.site.register(SearchClick)
admin.site.register(AlbumClick)
admin.site.register(ShareClick)
