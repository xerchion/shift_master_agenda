from django.db import models
from django.db.models.query import QuerySet

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
    amount = models.DecimalField(
        default=0.0, null=True, blank=True, decimal_places=2, max_digits=15
    )
    # este podria ser una referencia al de player...
    # player = models.CharField(default="", null=False, blank=False, max_length=20)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"Prize of {self.player} - {self.date} - {self.id} - Prize: {self.amount}"

    @classmethod
    def get_last_week_prize(cls) -> "Prize":
        return Prize.objects.latest("date")

    def get_last_player_prize(self, player: str | Player) -> float:
        """
        Retrieves the last prize for a player.

        Args:
            player  str | Player : The player's name or Player object.

        """
        if isinstance(player, str):
            player = Player.objects.get(name=player)
        query = Prize.objects.filter(player=player).order_by("-id").first()
        return query.amount if query else 0.0

    @classmethod
    def calculate_total_prizes(cls) -> float:
        return sum(element.amount for element in Prize.objects.all())

    @classmethod
    def get_prizes(cls) -> QuerySet["Prize"]:
        """Returns every Prize in history"""
        # TODO falta por ver como lo devuelvo, si como una lista o como
        return Prize.objects.all()
