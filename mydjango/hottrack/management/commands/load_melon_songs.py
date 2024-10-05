import json
from urllib.request import urlopen
from django.core.management import BaseCommand
from hottrack.models import Song
class Command(BaseCommand):
    help="Load songs from melon chart"
    def handle(self, *args,**options):
        melon_chart_url = "hottrack/melon-20230910.json"
        with open(melon_chart_url, "r", encoding="utf-8") as json_file:
            json_string = json_file.read()
        song_list=[Song.from_dict(song_dict) for song_dict in json.loads(json_string)]
        print("loaded song_list :",len(song_list))
        Song.objects.bulk_create(song_list,batch_size=100,ignore_conflicts=True)
        total=Song.objects.all().count()
        print("saved song_list :",total)