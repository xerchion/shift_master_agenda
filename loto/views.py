from datetime import datetime

from django.shortcuts import render

from .controllers.LotoController import LotoController
from .controllers.PlayerTurn import PlayerTurn
from .forms import SimplePrizeForm
from .models import Player, Prize


# Create your views here.
def loto_view(request):
    controller = LotoController()
    turn_controller = PlayerTurn(datetime.now())
    turns = turn_controller.generate_list_turns()

    # player_name = "Sergio"
    # player = Player.objects.get(name=player_name)

    # message = request.GET.get("data", "")
    # id = request.user.id
    if request.method == "POST":
        form = SimplePrizeForm(request.POST)
        if form.is_valid():
            prize = form.cleaned_data["prize"]
            prize = prize.replace(",", ".")

        else:
            print("formulario no valido")
        prize = float(prize)
        # grabar en premios
        last_week_player = turns["past"]
        date = datetime.now().date()
        last_week_player = Player.objects.get(name=last_week_player)
        Prize.objects.create(prize=prize, date=date, player=last_week_player)
    else:
        form = SimplePrizeForm()
    # Ejemple de suma de premios por jugador

    # premios = controller.calculate_player_prizes(player)
    # print("Suma de premios de : ", player_name, "es :", premios)

    # Ejemplo de lista de jugadores
    # players = Player.objects.all()
    # print("los jugadores en la vista: ", players)

    # Ejemple de Jugador al que le toca hechar la loteria
    # toca = PlayerTurn()
    # nombre = toca.get_current_turn_player()
    # print("la loteria le toca a: ", nombre)

    # EjemplO de suma total de premios
    total_prizes = Prize.calculate_total_prizes()
    # print("Suma de premios Total", total_prizes)

    # Ejemplo de suma total de gastos en loteria desde 1-enero-2023
    # total_spent = controller.calculate_total_spent()
    # print("Suma de gastos Total", total_spent)

    # Ejemplo de historial de premios
    # history_prizes = controller.get_prizes()
    # print("historial de premios", history_prizes)

    # Ejemplo de la reparto de premios por participante
    # money_for_player = controller.money_for_players()
    # print("Cantidad de dinero para cada uno: ", money_for_player)

    # Ejemplo de creación de formulario para meter el premio semanal

    form = SimplePrizeForm()

    # Ejemplo de set premio semanal, una vez obtenido
    # current_prize = 100  # dato que llegaria del get con el form,
    # en realidad el get no hace falta, el dato viene del form....
    # controller.set_week_prize(current_prize)

    # ejemplo de listado de players y sus premios
    players_and_prizes = controller.get_players_prizes()
    # print(players_and_prizes)

    # coger ultimo premio semanal
    last_prize = controller.get_last_prize(turns['last'])

    bets = controller.get_bets()
    context = {
        "players": players_and_prizes,
        "form": form,
        "turns": turns,
        "bets": bets,
        "total": total_prizes,
        "last_prize": last_prize,
    }
    # print("-----------------------------------")
    # print("Bets completos: ")
    return render(request, "loto.html", context)
