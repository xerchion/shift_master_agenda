from datetime import datetime

from ..config.constants import EURNOMILLONES, NACIONAL, PRIMITIVA
from ..models import Player, Prize
from .PlayerTurn import PlayerTurn


class LotoController:
    def calculate_player_prizes(self, player: Player) -> float:
        """
        Calculates the total sum of prizes for a specific player.

        """
        return sum(element.amount for element in Prize.objects.filter(player=player))

    def money_for_players(self) -> float:
        """
        Calculates and returns the money each player should receive.

        """
        total_amount = Prize.calculate_total_prizes()
        number_players = Player.objects.count()

        money_per_player = round(total_amount / number_players, 2)

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
        Prize.objects.create(amount=prize, date=date, player=player)

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
            total_prizes = self.calculate_player_prizes(player)

            # Append player information to the list
            player_and_prizes.append(
                {"name": player.name, "amount": total_prizes, "id": 0}
            )

        # Sort the list of players based on prize amount (descending order)
        player_and_prizes_sorted = sorted(
            player_and_prizes, key=lambda x: x["amount"], reverse=True
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
            primitiva_bets.append(add_separator(value))

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

    def get_last_prize(self, player: str | Player) -> float:
        """
        Retrieves the last prize for a player.

        Args:
            player :str | Player The player's name or Player object.

        """
        if isinstance(player, str):
            player = Player.objects.get(name=player)
        query = Prize.objects.filter(player=player).order_by("-id").first()
        return query.amount if query else 0
