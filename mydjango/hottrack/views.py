from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
# Create your views here.

def index(request:HttpRequest)->HttpResponse:
    return render(request, template_name="hottrack/index.html",context={})


    