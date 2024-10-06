from django.contrib import admin
from .models import Song
from django.utils.html import format_html
from .utils.melon import get_likes_dict


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "artist_name",
        "album_name",
    ]
    list_display = [
        "cover_image",
        "name",
        "artist_name",
        "album_name",
        "genre",
        "like_count",
        "release_date",
    ]
    list_filter = ["genre", "release_date"]
    actions = ["update_like_count"]

    def cover_image(self, song):
        return format_html('<img src="{}" style="width: 50px;"/>', song.cover_url)
        # return format_html(
        #     format_string='<img src="{}" style=""/>', args=(song.cover_url,)
        # )

    def update_like_count(self, request, queryset):
        melon_uid_list = queryset.values_list("melon_uid", flat=True)
        likes_dict = get_likes_dict(melon_uid_list)
        count = 0
        for song in queryset:
            if song.like_count != likes_dict.get(song.melon_uid):
                song.like_count = likes_dict.get(song.melon_uid)
                count += 1
        Song.objects.bulk_update(queryset, fields=["like_count"])
        self.message_user(request, f"{count}곡 갱신됨 ㅇㅇ")


# admin.site.register(Song,SongAdmin)
