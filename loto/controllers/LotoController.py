from datetime import datetime

from ..config.constants import EURNOMILLONES, NACIONAL, PRIMITIVA
from ..models import Player, Prize
from .PlayerTurn import PlayerTurn


class LotoController:
    def calculate_player_prizes(self, player):
        """
        Calculates the total sum of prizes for a specific player.

        Args:
            player: The player object for which prizes are being calculated.

        Returns:
            total (float): The total sum of prizes for the player.
        """
        total = 0

        # Iterate through all prizes associated with the player
        for prize in Prize.objects.filter(player=player):
            total += prize.prize  # Add the prize amount to the total

        return total

    def calculate_total_prizes(self):
        """
        Calculates the total sum of prizes for all players.

        Returns:
            total (float): The total sum of prizes for all players.
        """

        total = 0  # Initialize the total to zero

        # Iterate through all prizes
        for prize in Prize.objects.all():
            total += prize.prize

        return total

    def calculate_total_spent(self):
        # TODO faltaria sumar la cantidad que teniamos de antes, pero eso ya en la vista
        """Returns the Total Spent money from 1-1-2023"""

        weeks = PlayerTurn().current_week_number()
        return weeks * 17

    def get_prizes(self):
        """Returns every Prize in history"""
        # TODO falta por ver como lo devuelvo, si como una lista o como
        return Prize.objects.all()

    def money_for_players(self):
        """
        Calculates and returns the money each player should receive.

        Returns:
            float: The amount of money per player.
        """
        total = self.calculate_total_prizes()
        number_players = Player.objects.count()

        # Calculate the amount of money per player and round to two decimal places
        money_per_player = round(total / number_players, 2)

        return money_per_player

    def set_week_prize(self, prize):
        """
        Sets the prize for the current week.

        Args:
            prize (float): The prize amount.

        """
        date = datetime.now()

        # 2. Get the player who played last week
        last_player = PlayerTurn().other_week_player(-1)
        player = Player.objects.get(name=last_player)

        # 3. Create a new prize entry with provided prize, date, and player
        Prize.objects.create(prize=prize, date=date, player=player)

    def get_players_prizes(self):
        """
        Retrieves a list of players along with their corresponding prizes.

        Returns:
            list: A list of dictionaries,
            each containing player information (name, prize, id).
        """
        player_and_prizes = []

        # Iterate through each player
        for player in Player.objects.all():
            # Calculate the total prizes for the player
            prize = self.calculate_player_prizes(player)

            # Append player information to the list
            player_and_prizes.append({"name": player.name, "prize": prize, "id": 0})

        # Sort the list of players based on prize amount (descending order)
        player_and_prizes_sorted = sorted(
            player_and_prizes, key=lambda x: x["prize"], reverse=True
        )

        # Add an 'id' field to each player for identification
        # TODO esta funcion pdria refactorizarse sacandola de aqui y creando el campo
        # id en ella a la vez que mete el valor. Entonces arriba el id se lo quitabamos....
        players = []
        for i, player in enumerate(player_and_prizes_sorted):
            player["id"] = i + 1
            players.append(player)

        return players

    def get_bets(self):
        def add_separator(origin):
            result = ""
            for i, num in enumerate(origin):
                sign = "-"
                if i == len(origin) - 1:
                    sign = ""
                result += str(num) + sign
            return result

        apuestas_primitiva = []
        for ap, val in PRIMITIVA.items():
            apuesta = add_separator(val)

            # print(apuesta)
            apuestas_primitiva.append(apuesta)
        apuestas_euromillones = []
        for elemento in EURNOMILLONES:
            apuesta_numeros = add_separator(elemento["numeros"])
            apuesta_estrellas = add_separator(elemento["estrellas"])
            apuesta = apuesta_numeros + ", Estrellas: " + apuesta_estrellas
            apuestas_euromillones.append(apuesta)
        bets = {
            "nacional": NACIONAL,
            "primitiva": apuestas_primitiva,
            "euromillones": apuestas_euromillones,
        }
        return bets

    def get_last_week_prize(self):
        prize = Prize.objects.latest("date")
        return prize
