from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("compare-data/", include("kt_comparison.urls")),
]
