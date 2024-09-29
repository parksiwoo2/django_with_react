# mydjango.py
import sys
import django
import requests
from django.conf import settings
from django.core.management import execute_from_command_line
# from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.db import connection
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="secret",
    DATABASES={
        "default":{
            "ENGINE":"django.db.backends.sqlite3",
            "NAME":"melon-20230906.sqlite3",
        },
    },
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
        }
    ],
)
django.setup()

class Song(models.Model):
    id=models.AutoField(primary_key=True)
    가수=models.CharField(max_length=100)
    곡일련번호=models.CharField(max_length=100)
    순위=models.IntegerField()
    앨범=models.IntegerField()
    좋아요=models.CharField(max_length=200)
    커버이미지_주소=models.IntegerField()
    곡명=models.URLField()
    class Meta:
        db_table="songs"
        app_label="melon"
def index(request):
    """query=request.GET.get("query","").strip()
    song_list=Song.objects.all() #query set
    if query:
        song_list=song_list.filter(
            Q(곡명__icontains=query) | Q(가수__icontains=query)
        )
    song_list_data=list(song_list.values())"""
    return render(request, "index.html")

def song_list_api(request):
    query=request.GET.get("query","").strip()
    song_list=Song.objects.all() #query set
    if query:
        song_list=song_list.filter(
            Q(곡명__icontains=query) | Q(가수__icontains=query)
        )
    song_list_data=list(song_list.values())
    return JsonResponse(
        song_list_data,
        safe=False,
        json_dumps_params={"ensure_ascii":False},
        content_type="application/json; charset=utf-8",
    )
urlpatterns = [
    path("", index),
    path("api/song-list.json",song_list_api)
]
"""def get_song(query: str):
    cursor=connection.cursor()
    if query:
        param='%'+query+'%'
        sql=f"SELECT * FROM songs WHERE 가수 LIKE %s OR 곡명 LIKE %s"
        cursor.execute(sql,[param,param])
    else:
        cursor.execute(f"SELECT * FROM songs")
    column_names=[desc[0] for desc in cursor.description]
    song_list=[]
    for song_tuple in cursor.fetchall():
        song_dict=dict(zip(column_names,song_tuple))
        song_list.append(song_dict)
    return song_list"""
execute_from_command_line(sys.argv)