from django.apps import apps
from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase
from django.urls import reverse

from .config.constants import (BASE_DAY_COLORS, EVENING, FIRST, FREE_DAY, LAST,
                               NIGHT)
from .config.test_mocks import (DATE_STR, DATE_TEST, DAY_ATTRS, DAY_INDEX,
                                DAYS_IN_MONTH, END_PATTERN, HTTP_OK, MODELS,
                                MONTH, MONTH_ATTRS, MONTH_INDEX, PASSWORD,
                                RECAP_BASE_MONTH, RECAP_BASE_YEAR,
                                SCHEDULE_ATTRS, SHIFT_ATTRS, SLICE_SIZE,
                                START_PATTERN, TEAM, USERNAME,
                                VIEWS_WITH_LOGIN, VIEWS_WITHOUT_LOGIN, YEAR)
from .controllers.alterDayController import AlterDayController
from .controllers.UserAdapter import UserAdapter
from .forms import AlterDayForm
from .logic.Pattern import Pattern
from .logic.Schedule import Schedule
from .models import AlterDay, Color, MyUser

# tests de prueba nueva funcionalidad:


class TestPrueba(TestCase):
    def OK_test_TestCountersRecap_TEMPORALY(self):
        schedule = Schedule(YEAR, TEAM, BASE_DAY_COLORS)
        month = schedule.months[1]
        recap = month.calculate_recap()
        re = month.create_recap()
        atributos = [
            attr
            for attr in dir(recap)
            if not callable(getattr(recap, attr)) and not attr.startswith("__")
        ]
        atributos_re = [
            attr
            for attr in dir(re)
            if not callable(getattr(re, attr)) and not attr.startswith("__")
        ]
        if len(atributos) != len(atributos_re):
            print(len(atributos), "////", len(atributos_re))
            assert False, "nO TIENE LOS MISMOS ATRIBUTOS"
        if recap == re:
            assert False, "todo correcto"
        else:
            for atributo in atributos:
                if getattr(recap, atributo) == getattr(re, atributo):
                    print(f"Los tributos '{atributo}' son iguales en ambos objetos.")
                    print("tODO CORRECTO")

                else:
                    print(
                        f"Los atributos '{atributo}' no son iguales en ambos objetos."
                    )
                    print(getattr(recap, atributo), "----", getattr(re, atributo))


#  Logic Tests_______________________________________________________________


class PatternTest(TestCase):
    def test_pattern(self):
        # Check the first 7 days and last ones of the year 2023 and team C

        new_pattern = Pattern(YEAR, TEAM).pattern

        self.assertEqual(new_pattern[0:SLICE_SIZE], START_PATTERN)
        self.assertEqual(new_pattern[-SLICE_SIZE:], END_PATTERN)


class ScheduleTest(TestCase):
    def setUp(self):
        self.schedule = Schedule(YEAR, TEAM, BASE_DAY_COLORS)

    def test_integrity_attrs_schedule(self):
        def check_integrity_attrs(object, obj_attrs):
            """Check that the attributes of an object have not changed."""
            attrs = [
                attr
                for attr in dir(object)
                if not callable(getattr(object, attr)) and not attr.startswith("__")
            ]
            # print(attrs)
            name = type(object).__name__
            message = "La integridad de: " + name + "ha cambiado"
            self.assertEqual(attrs, obj_attrs, message)

        # Schedule integrity
        check_integrity_attrs(self.schedule, SCHEDULE_ATTRS)
        # Month
        check_integrity_attrs(self.schedule.months[MONTH_INDEX], MONTH_ATTRS)
        # Day
        check_integrity_attrs(
            self.schedule.months[MONTH_INDEX].days[DAY_INDEX], DAY_ATTRS
        )
        # Shift
        check_integrity_attrs(
            self.schedule.months[MONTH_INDEX].days[DAY_INDEX].shift, SHIFT_ATTRS
        )

    def test_months_len(self):
        number_of_months = len(self.schedule.months)
        self.assertEqual(number_of_months, 12)

    def test_type_month(self):
        type_month = type(self.schedule.months[MONTH_INDEX]).__name__
        self.assertEqual(type_month, "Month")

    def test_last_day_month(self):
        last_month_day = self.schedule.months[MONTH_INDEX].days[LAST].date.day
        self.assertEqual(last_month_day, DAYS_IN_MONTH)
        self.assertEqual(len(self.schedule.months[MONTH_INDEX].days), last_month_day)

    def test_shift_ok(self):
        # On 4th May 2023 the team C is free shift ("D") FREE_DAY
        self.assertEqual(self.schedule.months[4].days[3].shift.primal, FREE_DAY)

    def test_holidays(self):
        # August 29 Loja Fair
        self.assertEqual(self.schedule.months[8].days[28].holiday, True)
        # february 28 day of Andalusia
        self.assertEqual(self.schedule.months[2].days[27].holiday, True)
        # And first day of May is holiday. It´s the worker´s day
        self.assertEqual(self.schedule.months[5].days[FIRST].holiday, True)


class RecapTests(TestCase):
    def setUp(self):
        self.schedule = Schedule(YEAR, TEAM, BASE_DAY_COLORS)
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)

    def check_recap(self, calculate, data):
        recap = calculate()
        # Loop through the data dictionary and check each field in recap
        for key, value in data.items():
            self.assertEqual(getattr(recap, key), value, "Falla este campo: " + key)

    def test_base_recap_month(self):
        data = RECAP_BASE_MONTH
        self.check_recap(self.schedule.months[10].create_recap, data)

    def test_base_recap_year(self):
        data = RECAP_BASE_YEAR
        self.check_recap(self.schedule.calculate_recap_year, data)

    def test_alter_day_recap(self):
        # original day has "morning" shift, I put "evening (T)"
        day = AlterDay(
            user=self.user,
            date=DATE_TEST,
            shift=EVENING,
            keep_day=True,
            change_payable=False,
        )
        day.save()
        self.schedule.load_alter_days_db(self.user)
        data = {"extra_keep": 1}
        self.check_recap(self.schedule.months[MONTH_INDEX].create_recap, data)

        day = AlterDay(
            user=self.user,
            date=DATE_TEST,
            shift="D",
            keep_day=False,
            change_payable=False,
        )
        day.save()
        self.schedule.load_alter_days_db(self.user)

        data = {"extra_keep": 1}
        data = {
            "extra_payed": 0,
        }
        self.check_recap(self.schedule.months[MONTH_INDEX].create_recap, data)


# Model Tests_______________________________________________________________


class ModelsIntegrity(TestCase):
    def extract_current_models_integrity(self):
        """This method is for checking the current composition of the models:
        Name and number of fields.
        Use it only if the integrity test fails;
        this will indicate that some model has changed,
        and you will need to update the "data" field with the result of this method.
        Manually copy the console output into the "data" field of the integrity test.
        """
        data = {}
        models = apps.get_models()
        for model in models:
            model_name = model.__name__
            field_count = len(model._meta.fields)
            data[model_name] = field_count

    def test_model_integrity(self):
        for model in apps.get_models():
            number_of_fields = len(model._meta.fields)
            message = "Cambios en: " + model.__name__
            self.assertEqual(number_of_fields, MODELS[model.__name__], message)


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear un usuario de ejemplo para usar en las pruebas
        User.objects.create_user(username=USERNAME, password=PASSWORD)

    def test_object_name_is_username(self):
        user = User.objects.get(id=1)
        expected_object_name = user.username
        self.assertEquals(expected_object_name, str(user))

    def test_user_creation(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)


class MyUserModelTest(TestCase):
    def test_my_user_creation(self):
        user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        my_user = MyUser.objects.create(
            user=user,
            user_name=USERNAME,
            team="A",
            name="Juan",
            second_name="Sierra",
            category=1,
            password=PASSWORD,
        )

        self.assertEqual(my_user.user, user)
        self.assertEqual(my_user.user_name, USERNAME)
        self.assertEqual(my_user.team, "A")
        self.assertEqual(my_user.name, "Juan")
        self.assertEqual(my_user.second_name, "Sierra")
        self.assertEqual(my_user.category, 1)
        self.assertEqual(my_user.password, PASSWORD)


class AlterDayModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.schedule = Schedule(YEAR, TEAM, BASE_DAY_COLORS)
        self.day = AlterDay.objects.create(
            shift=NIGHT, user=self.user, date="2023-05-05"
        )

    def test_creation(self):
        alter_day = AlterDay.objects.create(shift=NIGHT, user=self.user)
        self.assertEqual(alter_day.shift, NIGHT)

    def test_modify(self):
        controller = AlterDayController(self.user.id, self.day.date, self.schedule)
        self.day.shift = EVENING
        form = AlterDayForm(instance=self.day)
        controller.save_day(form)

        day_modified = AlterDay.objects.get(user=self.user)
        self.assertEqual(self.day.shift, day_modified.shift)

    def test_restore(self):
        # whith alterDay exists
        controller = AlterDayController(self.user.id, self.day.date, self.schedule)
        self.assertEqual(controller.exists_day(), True)
        controller.restart_day()
        self.assertEqual(controller.exists_day(), False)
        # no exists
        controller = AlterDayController(self.user.id, "2023-01-01", self.schedule)
        self.assertEqual(controller.exists_day(), False)
        controller.restart_day()
        self.assertEqual(controller.exists_day(), False)


class ColorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.color = Color.objects.create(morning="Verde", user=self.user)

    def test_creation(self):
        color_db = Color.objects.get(user=self.user)
        self.assertEqual(color_db.morning, "Verde")

    def test_modify(self):
        old_color = self.color
        old_color.morning = "Blue"
        old_color.save()
        color_db = Color.objects.get(user=self.user)
        self.assertEqual(color_db.morning, "Blue")


# Views Tests_______________________________________________________________


class LoadViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        UserAdapter().add_new_user(USERNAME, PASSWORD, TEAM)

    def check_views(self, views):
        for view, text in views.items():
            response = self.client.get(reverse(view))
            self.assertEqual(response.status_code, HTTP_OK)
            self.assertContains(response, text)
        return response

    def test_views_without_login_required(self):
        response = self.check_views(VIEWS_WITHOUT_LOGIN)
        self.assertIsInstance(response.context["user"], AnonymousUser)

    def test_views_with_login_required(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        self.check_views(VIEWS_WITH_LOGIN)

    # views tests with arguments
    def test_recap_month_load(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        # This view has a month's number argument
        view_url = reverse("recap_month", kwargs={"month": MONTH})
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertContains(response, "Resumen de")

    def test_alter_day_load(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        # This view has a date argument
        argument = DATE_STR
        view_url = reverse("alter_day", kwargs={"date": argument})
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertContains(response, "Datos del turno")
