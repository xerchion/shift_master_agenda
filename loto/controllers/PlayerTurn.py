from datetime import datetime

from ..models import Player


class PlayerTurn:
    def __init__(self):
        self.players = Player.objects.all()
        self.players_names = [player.name for player in self.players]
        self.today = datetime.now()
        self.week = self.current_week_number()

    def current_week_number(self):
        """calculate and returns the number of week"""
        return self.today.isocalendar()[1]

    def get_current_turn_player(self):
        player_name = " "
        """Funcion que devuelve el nombre del participante al que le toca,
        calculado por semanas.

        """

        # print("Usuario en la bd dentro de get_current_turn_player...")
        # print(Player.objects.count())
        weeks_previous_years = 0
        if self.today.year > 2023:
            weeks_previous_years = self.calculate_total_weeks()
        # print("las semanas previas son: ", weeks_previous_years)
        # print("la self.week es: ", self.week)
        indice = self.get_index(self.week + weeks_previous_years)
        # print("El indice dentro de el usuario de esta semana es: ", indice)
        player_name = self.players[indice].name
        # print("el usuario es: ", player_name)
        return player_name

    def get_index(self, week):
        """
        Funcion que devuelve el inidce para la lista personas.
        Args:
            week (integer): numero de la semana que se quiere usar para el indice.
                        si es menor que la logitud de la lista, toma ese valor-1 sino
                        hace una division con resto para calcular el indice siguiendo
                        la serie.

        Returns:
            _type_: el numero de indice correcto para usar en la lista.
        """

        self.players = Player.objects.all()
        if week <= len(self.players):
            index = week - 1
            # print("lo coge del if")
        else:
            index = (week % len(self.players)) - 1

        return index

    def weeks_in_year(self, year):
        """Calcula las semanas totales que tiene un año. Recibe un
            numero de año como integer

        Returns:
            entero: la cantidad de semanas del año
        """
        first_day = datetime.datetime(year, 1, 1)
        last_day = datetime.datetime(year, 12, 31)
        return (last_day - first_day).days // 7 + 1

    def calculate_total_weeks(self):
        """Funcion que calcula las semanas totales desde 2023
        #TODO está sin probar, habra que probar en 2024 a ver si trabaja bien.
        #TODO o bien hacer test cambiando la fecha, en lugar de coger now ponerle una manual

        Returns:
            _type_: _description_
        """

        total_weeks = 0
        for year in range(2023, self.today.year - 1):
            total_weeks += self.year_weeks(year)
        return total_weeks

    def other_week_player(self, tam):
        player_name = ""
        player_now = self.get_current_turn_player()
        id_player_now = Player.objects.get(name=player_now).id

        player_name = Player.objects.get(id=id_player_now + (tam)).name

        return player_name

    def generate_list_turns(self):
        turns = {
            "past": self.other_week_player(-1),
            "current": self.get_current_turn_player(),
            "future": self.other_week_player(1),
        }
        return turns
