import json
from urllib.request import urlopen
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,get_object_or_404
from hottrack.models import Song
from django.db.models import QuerySet, Q
from hottrack.utils.cover import make_cover_image
from io import BytesIO
import pandas as pd
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
def cover_png(request, pk):
    # 최대값 512, 기본값 256
    canvas_size = min(512, int(request.GET.get("size", 256)))
    song = get_object_or_404(Song, pk=pk)
    cover_image = make_cover_image(
        song.cover_url, song.artist_name, canvas_size=canvas_size
    )
    # param fp : filename (str), pathlib.Path object or file object
    # image.save("image.png")
    response = HttpResponse(content_type="image/png")
    cover_image.save(response, format="png")
    return response
def export_csv(request: HttpRequest)-> HttpResponse:
    song_qs=Song.objects.all()
    df=pd.DataFrame(data=song_qs.values())
    export_file=BytesIO()
    df.to_csv(path_or_buf=export_file,index=False,encoding="utf-8-sig")
    response=HttpResponse(content=export_file.getvalue(),content_type="text/csv")
    response["Content-Disposition"]='attachment;filename="hottrack.csv"'
    return response
