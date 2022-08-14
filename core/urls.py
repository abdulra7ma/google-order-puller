from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Define Swagger API Schema
schema_view = get_schema_view(
    openapi.Info(
        title="ISAY FLY API",
        default_version="v1",
        description="",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


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
    re_path(
        r"^swagger/$",
        schema_view.with_ui(
            "swagger",
            cache_timeout=0,
        ),
        name="schema_swagger_ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui(
            "redoc",
            cache_timeout=0,
        ),
        name="schema_redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
