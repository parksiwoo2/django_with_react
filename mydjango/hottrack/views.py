import json
from urllib.request import urlopen
from django.http import HttpRequest,HttpResponse
from django.shortcuts import render
from hottrack.models import Song

def index(request: HttpRequest)-> HttpResponse:
    melon_chart_url="hottrack/melon-20230910.json"
    with open(melon_chart_url, 'r', encoding='utf-8') as json_file:
        json_string = json_file.read()
    song_list=[
        Song.from_dict(song_dict)
        for song_dict in json.loads(json_string)
    ]
    return render(
        request=request,
        template_name="hottrack/index.html",
        context={
            "song_list":song_list,
        },
    )