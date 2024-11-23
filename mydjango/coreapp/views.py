from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def index(request):
    messages.debug(request, message="디버그 메세지")
    messages.info(request, message="정보 메세지")
    messages.success(request, message="성공 메세지")
    messages.warning(request, message="경고 메세지")
    messages.error(request, message="에러 메세지")

    return render(request=request, template_name="core/index.html")
