from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "admin/doc/",
        include("django.contrib.admindocs.urls"),
    ),
    path(
        "",
        include("stats.urls"),
    ),
    path(
        "api/",
        include("stats.api.urls"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
