import json
from urllib.request import urlopen
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from hottrack.models import Song


def index(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("query", "").strip()
    melon_chart_url = "hottrack/melon-20230910.json"
    with open(melon_chart_url, "r", encoding="utf-8") as json_file:
        json_string = json_file.read()
    song_list = [Song.from_dict(song_dict) for song_dict in json.loads(json_string)]
    if query:
        queryl = query.lower()
        song_list = [
            song
            for song in song_list
            if (
                (queryl in song.name.lower())
                or (queryl in song.artist_name.lower())
                or (queryl in song.album_name.lower())
            )
        ]
    return render(
        request=request,
        template_name="hottrack/index.html",
        context={
            "song_list": song_list,
        },
    )
