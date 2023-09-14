from django.urls import path

from .views import loto_view

urlpatterns = [
    path("loto/", loto_view, name="loto"),
]
