from datetime import datetime

from django.db.models.query import QuerySet

from ..config.constants import EURNOMILLONES, NACIONAL, PRIMITIVA
from ..models import Player, Prize
from .PlayerTurn import PlayerTurn


class LotoController:
    def __init__(self):
        self.pppppp = 0  # borralo cuando tengas atributos de esta clase...

    def calculate_player_prizes(self, player: Player) -> float:
        """
        Calculates the total sum of prizes for a specific player.

        Args:
            player: The player object for which prizes are being calculated.

        Returns:
            total (float): The total sum of prizes for the player.
        """
        total = 0

        # Iterate through all prizes associated with the player
        for element in Prize.objects.filter(player=player):
            total += element.prize  # Add the prize amount to the total

        return total

    def calculate_total_prizes(self) -> float:
        """
        Calculates the total sum of prizes for all players.

        """

        total = 0  # Initialize the total to zero

        # Iterate through all prizes
        for element in Prize.objects.all():
            total += element.prize
        return total

    def get_prizes(self) -> QuerySet[Prize]:
        """Returns every Prize in history"""
        # TODO falta por ver como lo devuelvo, si como una lista o como
        return Prize.objects.all()

    def money_for_players(self) -> float:
        """
        Calculates and returns the money each player should receive.

        """
        total = self.calculate_total_prizes()
        number_players = Player.objects.count()

        # Calculate the amount of money per player and round to two decimal places
        money_per_player = round(total / number_players, 2)

        return float(money_per_player)

    def set_week_prize(self, prize: float | int) -> None:
        """
        Sets the prize for the last week.

        Args:
            prize (float): The prize amount.

        """
        date = datetime.now()

        # 2. Get the player who played last week
        last_player = PlayerTurn(date).last_player
        player = Player.objects.get(name=last_player)

        # 3. Create a new prize entry with provided prize, date, and player
        Prize.objects.create(prize=prize, date=date, player=player)

    def get_players_prizes(self) -> list[dict]:
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

        # Add an 'id' field its value to each player (ranking´s order)
        players = []
        for i, player in enumerate(player_and_prizes_sorted):
            player["id"] = i + 1
            players.append(player)
        return players

    def get_bets(self) -> dict:
        """
        Retrieves bets for different games.

        """

        def add_separator(origin: list[int]) -> str:
            """
            Adds a separator to a list of numbers.

            """
            result = ""
            for i, num in enumerate(origin):
                sign = "-"
                if i == len(origin) - 1:
                    sign = ""
                result += str(num) + sign
            return result

        primitiva_bets = []
        for _, value in PRIMITIVA.items():
            bet = add_separator(value)
            primitiva_bets.append(bet)

        euromillones_bet = []
        for element in EURNOMILLONES:
            numbers_bets = add_separator(element["numbers"])
            stars_bets = add_separator(element["stars"])
            bet = numbers_bets + ", Estrellas: " + stars_bets
            euromillones_bet.append(bet)

        bets = {
            "nacional": NACIONAL,
            "primitiva": primitiva_bets,
            "euromillones": euromillones_bet,
        }
        return bets

    def get_last_week_prize(self) -> Prize:
        """
        Retrieves the prize for the last week.

        """
        prize = Prize.objects.latest("date")
        return prize

    def get_last_prize(self, player: str | Player) -> float:
        """
        Retrieves the last prize for a player.

        Args:
            player :str | Player The player's name or Player object.

        """
        if isinstance(player, str):
            player = Player.objects.get(name=player)
        query = Prize.objects.filter(player=player).order_by("-id").first()
        return query.prize if query else 0
