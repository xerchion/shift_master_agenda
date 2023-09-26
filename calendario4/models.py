from django.contrib.auth.models import User
from django.db import models

from .config.constants import SHIFTS


class Team(models.Model):
    letter = models.CharField(max_length=1, default="", null=True, blank=True)
    text = models.CharField(max_length=8, default="", null=True, blank=True)
    color = models.CharField(max_length=15, default="", null=True, blank=True)

    def __str__(self):
        return str(self.text)


TEAMS_TUPLE = tuple(Team.objects.values_list("letter", "text"))


class Category(models.Model):
    number = models.IntegerField(null=False, blank=False, unique=True)
    text = models.CharField(max_length=50, default="", null=True, blank=True)
    precio1 = models.DecimalField(
        decimal_places=3, max_digits=3, default="", null=True, blank=True
    )

    def __str__(self):
        return str(self.text)


class MyUser(models.Model):
    CATEGORIES = tuple(Category.objects.values_list("number", "text"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(
        max_length=20,
        default="",
        null=True,
        blank=True,
        verbose_name="Nombre de Usuario:",
    )
    team = models.CharField(
        max_length=1,
        default=None,
        null=True,
        blank=True,
        verbose_name=" (Obligatorio) Turno",
        choices=TEAMS_TUPLE,
    )
    name = models.CharField(
        max_length=20,
        default="",
        null=True,
        blank=True,
        verbose_name="(Opcional) Nombre real",
    )
    second_name = models.CharField(max_length=20, default="", null=True, blank=True)
    category = models.IntegerField(
        default="0",
        null=True,
        blank=True,
        verbose_name="(Opcional) Categoria:",
        choices=CATEGORIES,
    )
    password = models.CharField(
        max_length=10, default="", null=True, blank=True, verbose_name="Contraseña:"
    )

    def __str__(self):
        return str(self.user_name)


class Color(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    morning = models.CharField(
        default="", max_length=8, verbose_name="Mañana ", null=True, blank=True
    )
    afternoon = models.CharField(
        default="", max_length=8, verbose_name="Tarde ", null=True, blank=True
    )
    night = models.CharField(
        default="", max_length=8, verbose_name="Noche ", null=True, blank=True
    )
    split_shift = models.CharField(
        default="", max_length=8, verbose_name="Jornada Partida ", null=True, blank=True
    )
    free = models.CharField(
        default="", max_length=8, verbose_name="Descanso ", null=True, blank=True
    )
    holiday = models.CharField(
        default="", max_length=8, verbose_name="Festivo ", null=True, blank=True
    )
    extra_holiday = models.CharField(
        default="", max_length=8, verbose_name="Extra-Festivo ", null=True, blank=True
    )


class AlterDay(models.Model):
    BOOL_OPTIONS = [
        (True, "Sí"),
        (False, "No"),
    ]
    BOOL_OPTIONS_EXTRA_DAY = [
        (True, "Guardarlo"),  # True option
        (False, "Cobrarlo"),  # False option
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=None, null=True, blank=True)

    shift = models.CharField(
        default=None,
        null=False,
        blank=False,
        max_length=1,
        verbose_name="Turno ",
        choices=SHIFTS,
    )
    overtime = models.CharField(
        default="0", null=True, blank=True, verbose_name="Horas extra ", max_length=2
    )
    comments = models.CharField(
        default="", max_length=200, null=True, blank=True, verbose_name="Comentarios "
    )
    keep_day = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="Dìa extra. ¿Qué prefieres?",
        choices=BOOL_OPTIONS_EXTRA_DAY,
    )
    change_payable = models.BooleanField(
        default=False,
        null=True,
        blank=False,
        choices=BOOL_OPTIONS,
        verbose_name="¿Plus de cambio de turno?",
    )


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
