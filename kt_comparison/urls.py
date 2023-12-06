from django.contrib import admin
from django.urls import path, include

from kt_comparison.views import IndexView, SubidFormView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('find-subid/', SubidFormView.as_view(), name='subid_check'),
]
