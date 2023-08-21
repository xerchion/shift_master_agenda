from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase
from django.urls import reverse

from .config.constants import BASE_DAY_COLORS
from .controllers.UserAdapter import UserAdapter
from .logic.Pattern import Pattern
from .logic.Schedule import Schedule
from .models import AlterDay, MyUser


class PatternTest(TestCase):
    def test_pattern(self):
        # Check the first 7 days and last ones of the year 2023 and team C
        start_pattern = ["T", "N", "N", "D", "D", "D", "D"]
        end_pattern = ["M", "M", "T", "T", "N", "N", "N"]

        new_pattern = Pattern(2023, "C").pattern

        self.assertEqual(new_pattern[0:7], start_pattern)
        self.assertEqual(new_pattern[-7:], end_pattern)


class ScheduleTest(TestCase):

    def test_months(self):
        schedule = Schedule(2023, "C", BASE_DAY_COLORS)
        number_of_months = len(schedule.months)
        self.assertEqual(number_of_months, 12)

    def test_type_month(self):
        schedule = Schedule(2023, "C", BASE_DAY_COLORS)
        type_month = type(schedule.months[5]).__name__
        self.assertEqual(type_month, "Month")

    def test_last_day_month(self):
        # February 2023 has 28 days
        schedule = Schedule(2023, "C", BASE_DAY_COLORS)
        last_month_day = schedule.months[1].days[-1].date.day
        self.assertEqual(last_month_day, 28)
        self.assertEqual(len(schedule.months[1].days), last_month_day)

    def test_shift_ok(self):
        # On 4th May 2023 the team C is free shift ("D")
        schedule = Schedule(2023, "C", BASE_DAY_COLORS)
        self.assertEqual(schedule.months[4].days[3].shift.primal, "D")

    def test_holidays(self):
        schedule = Schedule(2023, "C", BASE_DAY_COLORS)
        # August 29 Loja Fair
        self.assertEqual(schedule.months[8].days[28].holiday, True)
        # february 28 day of Andalusia
        self.assertEqual(schedule.months[2].days[27].holiday, True)
        # And first day of May is holiday. It´s the worker´s day
        self.assertEqual(schedule.months[5].days[0].holiday, True)


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear un usuario de ejemplo para usar en las pruebas
        User.objects.create_user(username="ejemplo", password="contraseña123")

    def test_object_name_is_username(self):
        user = User.objects.get(id=1)
        expected_object_name = user.username
        self.assertEquals(expected_object_name, str(user))

    def test_user_creation(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)


class MyUserModelTest(TestCase):
    def test_my_user_creation(self):
        user = User.objects.create_user(username="usuarioJuan",
                                        password="password")
        my_user = MyUser.objects.create(
            user=user,
            user_name="usuarioJuan",
            team="A",
            name="Juan",
            second_name="Sierra",
            category=1,
            password="password",
        )

        self.assertEqual(my_user.user, user)
        self.assertEqual(my_user.user_name, "usuarioJuan")
        self.assertEqual(my_user.team, "A")
        self.assertEqual(my_user.name, "Juan")
        self.assertEqual(my_user.second_name, "Sierra")
        self.assertEqual(my_user.category, 1)
        self.assertEqual(my_user.password, "password")


class AlterDayModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser",
                                             password="testpassword")

    def test_creation(self):
        alter_day = AlterDay.objects.create(shift="N", user=self.user)
        self.assertEqual(alter_day.shift, "N")

    def text_modify(self):
        ...

    def test_restore(self):
        ...


class RecapTests(TestCase):

    # Crea un schedule de ejemplo para usar en las pruebas
    schedule = Schedule(2023, "C", BASE_DAY_COLORS)

    def check_recap(self, calculate, data):
        recap = calculate()
        # Loop through the data dictionary and check each field in recap
        for key, value in data.items():
            self.assertEqual(getattr(recap, key), value)

    def test_recap_month(self):
        # November data test
        data = {
            "name": "Noviembre",
            "number_of_days": 30,
            "mornings": 4,
            "evenings": 5,
            "nights": 7,
            "workings": 16,
            "frees": 14,
            "holidays": 1,
            "extra_holidays": 1,
            "holidays_not_worked": 0,
            "change_payables": 0,
            "keep_days": 0,
            "overtimes": 0
        }
        self.check_recap(self.schedule.months[10].calculate_recap, data)

    def test_recap_year(self):
        # 2023 data test
        data = {
            "name": 2023,
            "number_of_days": 365,
            "mornings": 72,
            "evenings": 73,
            "nights": 75,
            "workings": 220,
            "frees": 145,
            "holidays": 15,
            "extra_holidays": 6,
            "holidays_not_worked": 9,
            "change_payables": 0,
            "keep_days": 0,
            "overtimes": 0
        }
        self.check_recap(self.schedule.calculate_recap_year, data)


class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'Perico'
        self.password = 'Palotes'
        self.team = "C"
        self.user_adapter = UserAdapter()
        self.user = self.user_adapter.add_new_user(self.username,
                                                   self.password, self.team)

    def check_views(self, views):
        for view, text in views.items():
            response = self.client.get(reverse(view))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, text)
        return response

    # views tests without user required
    def test_no_logged_in_user(self):
        views = {
            # Key: view name
            # Value: text to search in the view
            'home': 'Bienvenido',
            'signup': 'Registro de Nuevo Usuario',
        }
        response = self.check_views(views)
        self.assertIsInstance(response.context['user'], AnonymousUser)

    # views tests with user required
    def test_load_views(self):
        views = {
            # Key: view name
            # Values: text to search in the view
            'agenda': 'Calendario',
            'config': 'Datos Personales',
            'recap_year': 'Resumen de',
            'signup': 'Registro de Nuevo Usuario',
            'change_pass': 'Cambio de contraseña',
            'change_color_days': 'Cambio de Colores'
        }
        self.client.login(username=self.username, password=self.password)
        self.check_views(views)

    # views tests with arguments
    def test_recap_month_load(self):
        self.client.login(username=self.username, password=self.password)
        # This view has a month's number argument
        month = "1"
        view_url = reverse('recap_month', kwargs={'month': month})
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resumen de")

    def test_alter_day_load(self):
        self.client.login(username=self.username, password=self.password)
        # This view has a date argument
        argument = "2023-02-02"
        view_url = reverse('alter_day', kwargs={'date': argument})
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Datos del turno")
