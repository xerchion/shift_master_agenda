from django.urls import path

from .views import players_view

urlpatterns = [
    path("players_view/", players_view, name="players_view"),
]
