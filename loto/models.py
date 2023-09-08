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


class Prize(models.Model):
    date = models.DateField(default=None, null=True, blank=True)
    prize = models.DecimalField(
        default=0.0, null=True, blank=True, decimal_places=2, max_digits=15
    )
    # este podria ser una referencia al de player...
    # player = models.CharField(default="", null=False, blank=False, max_length=20)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
