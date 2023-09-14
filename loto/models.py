from django.db import models

from calendario4.models import TEAMS_TUPLE


class Player(models.Model):
    name = models.CharField(default="", null=False, blank=False, max_length=20)
    team = models.CharField(
        max_length=1,
        default=None,
        null=True,
        blank=True,
        verbose_name=" (Obligatorio) Turno",
        choices=TEAMS_TUPLE,
    )

    def __str__(self):
        return str(self.name)

    def get_last_turn_player(self) -> str:
        """
        Obtains the name of the player who had the last turn.
        """
        index = self.get_index(self.week - 1)
        return self.players[index].name


class Prize(models.Model):
    date = models.DateField(default=None, null=True, blank=True)
    prize = models.DecimalField(
        default=0.0, null=True, blank=True, decimal_places=2, max_digits=15
    )
    # este podria ser una referencia al de player...
    # player = models.CharField(default="", null=False, blank=False, max_length=20)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    # TODO NO USADA, PERO CREEO QUE ES UTIL
    @classmethod
    def get_last_week_prize(cls) -> "Prize":
        """
        Retrieves the prize for the last week.

        """
        prize = Prize.objects.latest("date")
        return prize

    def get_last_player_prize(self, player: str | Player) -> float:
        """
        Retrieves the last prize for a player.

        Args:
            player  str | Player : The player's name or Player object.

        """
        if isinstance(player, str):
            player = Player.objects.get(name=player)
        query = Prize.objects.filter(player=player).order_by("-id").first()
        return query.prize if query else 0.0

    @classmethod
    def calculate_total_prizes(cls) -> float:
        """
        Calculates the total sum of prizes for all players.

        """

        total = 0  # Initialize the total to zero

        # Iterate through all prizes
        for element in Prize.objects.all():
            total += element.prize
        return total
