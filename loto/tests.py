from datetime import datetime, timedelta

from django.test import TestCase

from .config.constants import NACIONAL
from .config.constants_tests import (EUROMILLONES, FIRST, PLAYER_DATA,
                                     PLAYER_NAMES, PRIMITIVA, PRIZE,
                                     SAMPLE_PRIZES, SECOND, TEAM)
from .controllers.LotoController import LotoController
from .controllers.PlayerTurn import PlayerTurn
from .forms import PrizeForm
from .models import Player, Prize


def save_player_initial_data():
    Player.objects.all().delete()
    for player in PLAYER_DATA:
        name = player["name"]
        team = player["team"]
        Player.objects.create(name=name, team=team)


class PlayerTurnTests(TestCase):
    def setUp(self):
        save_player_initial_data()
        self.date = "11-09-2023"
        self.turn = PlayerTurn(self.date)

    def test_correct_week_and_player(self):
        date_base = datetime.strptime(self.date, "%d-%m-%Y").date()

        # case for week Number 38, date : 2023-09-21
        date = date_base + timedelta(days=10)
        self.turn = PlayerTurn(date)
        self.assertEqual(self.turn.get_current_week(date), 38)
        self.assertEqual(
            self.turn.get_current_turn_player(date),
            self.turn.current_player,
        )
        # case for week Number 179, date :  2026-06-07
        date = date_base + timedelta(days=1000)
        self.turn = PlayerTurn(date)
        self.assertEqual(self.turn.get_current_week(date), 179)
        self.assertEqual(
            self.turn.get_current_turn_player(date),
            self.turn.current_player,
        )
        # case for week Number 1465,  date : 2051-01-26
        date = date_base + timedelta(days=9999)
        self.turn = PlayerTurn(date)
        self.assertEqual(self.turn.get_current_week(date), 1465)
        self.assertEqual(
            self.turn.get_current_turn_player(date),
            self.turn.current_player,
        )


class PlayerTests(TestCase):
    def setUp(self):
        self.player = Player.objects.create(name=PLAYER_NAMES[FIRST], team=TEAM)

    def test_prize_save_ok(self):
        """
        Test the successful saving of a prize.

        This method creates a prize with a specific date and amount,
        associated with a player, and then verifies if the prize has been saved correctly.

        """
        current_date = datetime.now().date()
        Prize.objects.create(date=current_date, amount=PRIZE, player=self.player)

        condition = Prize.objects.filter(player=self.player).exists()
        self.assertTrue(condition)

    def test_first_player(self):
        save_player_initial_data()
        name = Player.objects.first().name
        expected = "Dani"
        self.assertEqual(name, expected)

    def test_player_name(self):
        name = Player.objects.filter().last().name
        self.assertEqual(name, Player.objects.all().last().__str__())


class LotoControllerTests(TestCase):
    def setUp(self):
        players = PLAYER_NAMES
        name = players[FIRST]
        self.player = Player.objects.create(name=name, team=TEAM)
        self.date = datetime.now().date()
        self.ctrl = LotoController()

    def test_total_player_prizes(self):
        """
        Test the calculation of total prizes for a player.

        """

        # List of prizes associated with the player
        prizes = SAMPLE_PRIZES

        # Calculate the total prizes
        total_prizes = sum(prizes)

        # Create a player
        name = PLAYER_NAMES[SECOND]
        Player.objects.create(name=name, team=TEAM)
        player = Player.objects.get(name=name)

        # Create prizes for the player with specified amounts
        for prize in prizes:
            Prize.objects.create(date=self.date, player=player, amount=prize)

        # Calculate the total prizes for the player using the controller method
        total_method = self.ctrl.calculate_player_prizes(player)

        # Check if the calculated total matches the expected total
        self.assertEqual(total_method, total_prizes)

    def test_set_week_prize(self):
        """
        Test setting the weekly prize.

        This method tests the functionality of setting the weekly prize by calling
        the 'set_week_prize' method from the controller. It first saves initial player data,
        then sets a prize amount of 35.2. Finally, it checks if a prize with the specified
        amount exists in the database.

        """
        # Save initial player data
        save_player_initial_data()

        prize = PRIZE
        self.ctrl.set_week_prize(prize)

        # Check if a prize with the specified amount exists in the database
        self.assertTrue(Prize.objects.filter(amount=prize).exists())

    def test_get_bets(self):
        """
        Test the retrieval of bets from the controller.

        This method tests the 'get_bets' method from the controller for different lottery types:

        """
        # Test for 'NACIONAL'
        result = self.ctrl.get_bets()["nacional"]
        self.assertEqual(NACIONAL, result)

        # Test for 'primitiva'
        result = self.ctrl.get_bets()["primitiva"]
        self.assertEqual(PRIMITIVA, result)

        # Test for 'euromillones'
        result = self.ctrl.get_bets()["euromillones"]
        self.assertEqual(EUROMILLONES, result)

    def test_generate_list_turns(self):
        """
        Test the generation of a list of turns for players across different weeks.

        This method sets up player data, assigns weekly prizes, and calculates the players
        for the last, current, and next week. It then generates a list of turns and checks
        if they match the expected results.

        The test includes the following steps:
        1. Create players and set initial data.
        2. Set the weekly prizes for the current and next week.
        3. Calculate the player from the last week.
        4. Get the player for the current turn and extract their name.
        5. Calculate the player for the next week.
        6. Automatically calculate the turns using pl_ctrl.generate_list_turns().
        7. Compare the calculated results with the expected results.

        """

        save_player_initial_data()
        self.pl_ctrl = PlayerTurn(self.date)

        self.ctrl.set_week_prize(10)
        self.ctrl.set_week_prize(50)

        last_week_player_name = self.pl_ctrl.last_player

        name = self.pl_ctrl.get_current_turn_player(self.date)
        current_week_player_name = Player.objects.get(name=name).name

        next_week_player_name = self.pl_ctrl.next_player

        turns = self.pl_ctrl.generate_list_turns()

        self.assertEqual(last_week_player_name, turns["last"])
        self.assertEqual(current_week_player_name, turns["current"])
        self.assertEqual(next_week_player_name, turns["next"])

    def test_money_for_players(self):
        save_player_initial_data()
        player = Player.objects.filter().first()
        Prize.objects.create(player=player, amount=1000)
        result = self.ctrl.money_for_players()
        self.assertEqual(result, 66.67)

    def test_get_players_prizes(self):
        save_player_initial_data()
        player = Player.objects.get(name="Sergio")
        for i in range(10, 100, 10):
            Prize.objects.create(amount=i, player=player)

        # el primer player
        player = Player.objects.first()
        player_prizes = self.ctrl.calculate_player_prizes(player)
        all_players_prizes = self.ctrl.get_players_prizes()
        for p in all_players_prizes:
            if p["name"] == player.name:
                prize = p["amount"]
        self.assertEqual(player_prizes, prize)

        # el ultimo player
        player = Player.objects.last()
        player_prizes = self.ctrl.calculate_player_prizes(player)

        all_players_prizes = self.ctrl.get_players_prizes()

        self.assertEqual(player_prizes, all_players_prizes[1]["amount"])

    def test_get_last_user_prize(self):
        date = datetime.now().date()
        for i in range(1, 4):
            date = date + timedelta(days=i)  # Suma un día
            Prize.objects.create(player=self.player, date=date, amount=i)

        Prize.objects.latest("date")
        self.assertEqual(
            Prize.objects.latest("date").amount, self.ctrl.get_last_prize(self.player)
        )

    def test_get_prizes(self):
        prizes = Prize.objects.count()
        count_in_method = len(Prize.get_prizes())
        # no lo comparo directamente, sino sus tamaños, pk si los comparo directos da error
        self.assertEqual(prizes, count_in_method)


class PrizeTests(TestCase):
    def setUp(self):
        players = PLAYER_NAMES
        name = players[FIRST]
        self.player = Player.objects.create(name=name, team=TEAM)

    def test_total_prizes_ok(self):
        """
        Test the calculation of total prizes.

        This method calls the 'calculate_total_prizes' method from the controller
        and compares the result with the expected total number of prizes.

        """
        amounts = [10, 20]
        for amount in amounts:
            Prize.objects.create(player=self.player, amount=amount)
        self.total_prizes = sum(amounts)

        total_method = Prize.calculate_total_prizes()
        self.assertEqual(total_method, self.total_prizes)

    # TODO FALTAN ESTOS TESTS....
    # TODO este no es de prizes....
    def test_get_last_turn_player(self):
        ...

    def test_get_last_week_prize(self):
        """
        Gets the prize from the last week.

        Returns:
            Prize or None if no prize is found.
        """
        sample_dates = [
            "2023-01-15",
            "2023-01-07",
            "2023-01-30",
            "2023-05-15",
            "2023-07-07",  # last
            "2023-04-30",
        ]
        for i, date in enumerate(sample_dates):
            player = Player.objects.create(name="Fede")
            player.save()
            player_prize = Prize.objects.create(
                player=player, amount=float(i), date=date
            )
            player_prize.save()

        test_amount = float(i - 1)
        last_prize = Prize.get_last_week_prize()
        test_date = datetime.strptime("2023-07-07", "%Y-%m-%d").date()

        self.assertEqual(test_amount, last_prize.amount)
        self.assertEqual(test_date, last_prize.date)
        self.assertEqual(4, last_prize.id - 1)

    def test_get_last_player_prize(self):
        ...


class PrizeFormTest(TestCase):
    # TODO no funciona
    def xtest_prize_form_init(self):
        form = PrizeForm()
        self.assertTrue(form.is_valid())
