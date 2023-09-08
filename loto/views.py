from django.shortcuts import render

from .models import Player


# Create your views here.
def players_view(request):
    players = Player.objects.all()
    print(players)
    context = {"players": players}
    return render(request, "hola.html", context)
