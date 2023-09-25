from datetime import datetime, timedelta

from ..config.constants import INITIAL_DATE
from ..models import Player


class PlayerTurn:
    def __init__(self, date):
        self.players = Player.objects.all()
        self.players_names = [player.name for player in self.players]
        if type(date) == str:
            self.date = datetime.strptime(date, "%d-%m-%Y")
        else:
            self.date = date
        self.week = self.get_current_week(self.date)
        self.current_player = self.get_current_turn_player(self.date)
        self.last_player = self.__get_last_turn_player()
        self.next_player = self.__get_next_turn_player()

    def get_current_turn_player(self, date) -> str:
        """Returns the name of the participant who is currently up,
        calculated by weeks.

        Args:
            date (datetime.date): The current date.

        Returns:
            str: The name of the player whose turn it is.

        """
        week_number = self.get_current_week(date)
        index = self.get_index(week_number)
        return self.players[index].name

    def get_current_week(self, date: datetime) -> int:
        """Returns the current week number based on the provided date.

        Args:
            date (datetime.date): The date for which to determine the week.

        Returns:
            int: The current week number.

        """
        if isinstance(date, datetime):
            date = date.date()

        # initial´s values
        monday = datetime.strptime(INITIAL_DATE, "%Y-%m-%d").date()
        sunday = monday + timedelta(days=6)
        week_number = 1

        while not (monday <= date <= sunday):
            week_number += 1
            monday = sunday + timedelta(days=1)
            sunday = monday + timedelta(days=6)
        return week_number

    def get_index(self, week: int) -> int:
        """
        Returns the index for the list of individuals.

        Args:
            week (int): The week number to use as the index.
                        It calculates the index following the series using modulo operation.
        """
        return week % len(self.players)

    def __get_last_turn_player(self) -> str:
        """
        Obtains the name of the player who had the last turn.
        """
        index = self.get_index(self.week - 1)
        return self.players[index - 1].name

    def __get_next_turn_player(self) -> str:
        """
        Obtains the name of the player who will have the next turn.
        """
        index = self.get_index(self.week + 1)
        return self.players[index].name

    def generate_list_turns(self) -> dict:
        """
        Generates a dictionary containing information about the last, current,
        and next players' turns.

        Returns:
            dict: A dictionary with keys "last", "current", and "next",
            each corresponding to a player's name.
        """
        turns = {
            "last": self.last_player,
            "current": self.get_current_turn_player(self.date),
            "next": self.next_player,
        }
        return turns
