import json
from urllib.request import urlopen
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from hottrack.models import Song
from django.db.models import QuerySet, Q


def index(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("query", "").strip()
    # melon_chart_url = "hottrack/melon-20230910.json"
    # with open(melon_chart_url, "r", encoding="utf-8") as json_file:
    #     json_string = json_file.read()
    # song_list = [Song.from_dict(song_dict) for song_dict in json.loads(json_string)]
    # if query:
    #     queryl = query.lower()
    #     song_list = [
    #         song
    #         for song in song_list
    #         if (
    #             (queryl in song.name.lower())
    #             or (queryl in song.artist_name.lower())
    #             or (queryl in song.album_name.lower())
    #         )
    #     ]
    song_qs: QuerySet = Song.objects.all()
    if query:
        song_qs = song_qs.filter(
            Q(name__icontains=query)
            | Q(artist_name__icontains=query)
            | Q(album_name__icontains=query)
        )
    return render(
        request=request,
        template_name="hottrack/index.html",
        context={
            "song_list": song_qs,
        },
    )