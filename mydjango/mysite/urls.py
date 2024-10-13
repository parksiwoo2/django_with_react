from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path(route="hottrack/", view=include("hottrack.urls")),
    path(route="", view=lambda request: redirect("/hottrack/")),
    path(route="coreapp/", view=include("coreapp.urls")),
]
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
