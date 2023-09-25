from django.apps import apps
from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from .config.const_tests import (DATE_STR, DATE_TEST, DAY_ATTRS, DAY_INDEX,
                                 DAYS_IN_MONTH, END_PATTERN, HTTP_OK, MODELS,
                                 MONTH, MONTH_ATTRS, MONTH_INDEX, PASSWORD,
                                 RECAP_ATTRS, RECAP_BASE_MONTH,
                                 RECAP_BASE_YEAR, SCHEDULE_ATTRS, SHIFT_ATTRS,
                                 SLICE_SIZE, START_PATTERN, TEAM, USERNAME,
                                 VIEWS_WITH_LOGIN, VIEWS_WITHOUT_LOGIN, YEAR)
from .config.constants import (BASE_DAY_COLORS, EVENING, FIRST, FREE_DAY, LAST,
                               NAME_USER_EXISTS, NIGHT)
from .controllers.AlterDayController import AlterDayController
from .controllers.UserAdapter import UserAdapter
from .controllers.utils import check_integrity_attrs, init_tables_constants
from .forms import AlterDayForm
from .logic.Month import Month
from .logic.Pattern import Pattern
from .logic.Recap import Recap
from .logic.Schedule import Schedule
from .models import AlterDay, Category, Color, MyUser, Team

#  Logic Tests_______________________________________________________________


class PatternTest(TestCase):
    def test_pattern(self):
        # Check the first 7 days and last ones of the year 2023 and team C

        new_pattern = Pattern(YEAR, TEAM).pattern

        self.assertEqual(new_pattern[FIRST:SLICE_SIZE], START_PATTERN)
        self.assertEqual(new_pattern[-SLICE_SIZE:], END_PATTERN)


class ScheduleTest(TestCase):
    def setUp(self):
        self.schedule = Schedule(YEAR, TEAM, BASE_DAY_COLORS)
        self.result = None
        self.message = None

    def test_integrity_attrs_schedule(self):
        # Schedule integrity
        result, message = check_integrity_attrs(self.schedule, SCHEDULE_ATTRS)
        self.assertTrue(result, message)

        # Month
        result, message = check_integrity_attrs(
            self.schedule.months[MONTH_INDEX], MONTH_ATTRS
        )
        self.assertTrue(result, message)

        # Day
        result, message = check_integrity_attrs(
            self.schedule.months[MONTH_INDEX].days[DAY_INDEX], DAY_ATTRS
        )
        self.assertTrue(result, message)

        # Shift
        result, message = check_integrity_attrs(
            self.schedule.months[MONTH_INDEX].days[DAY_INDEX].shift, SHIFT_ATTRS
        )
        self.assertTrue(result, message)

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

    def test_shifts_real_and_primal_equeal(self):
        day = self.schedule.months[FIRST].days[FIRST]
        self.assertAlmostEqual(day.shift.primal, day.shift_real)

    def test_holidays(self):
        # August 29 Loja Fair
        self.assertEqual(self.schedule.months[7].days[28].holiday, True)
        # february 28 day of Andalusia
        self.assertEqual(self.schedule.months[1].days[27].holiday, True)
        # And first day of May is holiday. It´s the worker´s day
        self.assertEqual(self.schedule.months[4].days[FIRST].holiday, True)


class RecapTests(TestCase):
    def setUp(self):
        self.schedule = Schedule(YEAR, TEAM, BASE_DAY_COLORS)
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)

    def check_recap(self, recap, data):
        # Loop through the data dictionary and check each field in recap
        for key, value in data.items():
            self.assertEqual(getattr(recap, key), value, "Falla este campo: " + key)

    def test_integrity_attrs_recap(self):
        result, message = check_integrity_attrs(Recap(), RECAP_ATTRS)
        self.assertTrue(result, message)

    def test_base_recap_month(self):
        # Checks that a specific month has its recap correctly.
        data = RECAP_BASE_MONTH
        month = Month.extract_month_number(RECAP_BASE_MONTH)
        month = self.schedule.months[month]
        recap = Recap.calculate(month, month.name)
        self.check_recap(recap, data)

    def test_base_recap_year(self):
        data = RECAP_BASE_YEAR
        recap = Recap.calculate(self.schedule.months, self.schedule.year)
        self.check_recap(recap, data)

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
        self.schedule = AlterDayController.load_alter_days_db(self.user, self.schedule)
        data = {"extra_keep": 1}
        month = self.schedule.months[MONTH_INDEX]
        recap = Recap.calculate(month, month.name)
        self.check_recap(recap, data)

        day = AlterDay(
            user=self.user,
            date=DATE_TEST,
            shift="D",
            keep_day=False,
            change_payable=False,
        )
        day.save()
        self.schedule = AlterDayController.load_alter_days_db(self.user, self.schedule)

        data = {"extra_keep": 1}
        data = {
            "extra_payed": 0,
        }
        month = self.schedule.months[MONTH_INDEX]
        recap = Recap.calculate(month, month.name)
        self.check_recap(recap, data)


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
        """
        Test the integrity of models.

        Checks if the models have the expected number of fields and are integrated properly.
        """

        for model in apps.get_models():
            number_of_fields = len(model._meta.fields)

            integration_message = f"The model {model.__name__} with {number_of_fields} fields is not integrated properly"
            self.assertTrue(model.__name__ in MODELS, integration_message)

            field_change_message = f"Changes in fields of: {model.__name__}"
            self.assertEqual(
                number_of_fields, MODELS[model.__name__], field_change_message
            )


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
        self.assertEqual(controller.check_if_day_exists(), True)
        controller.restart_day()
        self.assertEqual(controller.check_if_day_exists(), False)
        # no exists
        controller = AlterDayController(self.user.id, "2023-01-01", self.schedule)
        self.assertEqual(controller.check_if_day_exists(), False)
        controller.restart_day()
        self.assertEqual(controller.check_if_day_exists(), False)


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


# Utils Tests_______________________________________________________________
class UtilsTests(TestCase):
    def setUp(self):
        init_tables_constants()

    def test_category(self):
        cat_reg = Category.objects.get(number=1)
        self.assertEqual(cat_reg.text, "Tácnico Titulado Superior")

    def test_team(self):
        team_reg = Team.objects.get(letter="A")
        self.assertEqual(team_reg.text, "Turno A")


# Controllers Tests-----------------------------------------------------------------
# SignUpController Tests_______________________________________________________________


class SignUpViewTest(TestCase):
    def test_signup_view_user_ok(self):
        """
        Test the sign-up view to ensure that user registration works correctly.
        This test sends a POST request to the sign-up view with valid form data
        and checks that the view redirects to the configuration page.
        It also verifies that a new user is created in the database.
        """
        url = reverse("signup")
        response = self.client.post(
            url,
            data={
                "username": "user_test",
                "password": "pass_test",
                "repeat_pass": "pass_test",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="user_test").exists())

    def test_signup_view_user_exists(self):
        """
        Check if the user from the form is already in the database:

            Verify that, after the failure, it returns to the view.
            Confirm that the returned message is 'user already exists.'
            Check that the user has not been created in the database."
        """
        name = "user_test"
        psw = "pass_test"
        user = User(username=name, password=psw)
        user.save()
        url = reverse("signup")
        response = self.client.post(
            url,
            data={
                "username": name,
                "password": "other",
                "repeat_pass": "other",
            },
        )
        actual_message = response.context["msg"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(actual_message, NAME_USER_EXISTS)
        self.assertFalse(User.objects.filter(username="name", password="psw").exists())


# AlterDayController Tests_______________________________________________________________


class AlterDayControllerTests(TestCase):
    def setUp(self):
        date = DATE_STR  # Month is 11
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.schedule = Schedule(YEAR, TEAM, BASE_DAY_COLORS)
        self.controller = AlterDayController(self.user.id, date, self.schedule)

    def test_get_month_number(self):
        self.assertEqual(self.controller.get_month_number(), str(11))


class AlterDayViewTests(TestCase):
    def setUp(self):
        self.date = DATE_STR  # Month is 11
        adapter = UserAdapter()
        self.user = adapter.add_new_user(USERNAME, PASSWORD, TEAM).user
        self.schedule = Schedule(YEAR, TEAM, BASE_DAY_COLORS)
        self.controller = AlterDayController(self.user.id, self.date, self.schedule)
        self.response = self.client.login(username=USERNAME, password=PASSWORD)

    def test_alter_day_view_cancel_button_action(self):
        """
        Simulates Cancelar button press in form
        No accitions, no data to save
        """
        factory = RequestFactory()
        view_url = reverse("alter_day", kwargs={"date": DATE_STR})
        self.form = {
            "shift": ["T"],  # Shift is changed by test. Original is "M"
            "overtime": ["0"],
            "keep_day": ["False"],
            "change_payable": ["False"],
            "comments": [""],
            "Cancelar": ["Cancelar"],
        }
        # con client.post obtengo la funcionalidad, osea me redirecciona bien
        response = self.client.post(view_url, data=self.form)

        # con factory obtengo el contenido del request.POST, pero no redirecciona
        # creo que pk no acepta middleware o eso dice en la doc....
        respon = factory.post(view_url, data=self.form)

        # Un request tiene este tipo:      <class 'django.core.handlers.wsgi.WSGIRequest'>
        # y es el que tiene el QueryDict que es el atributo POST (request.POST)
        # AHI ESTAN LOS DATOS DE LA CONSULTA Y LO QUE DEVUELVE...

        # Redirection code ok?
        self.assertEqual(response.status_code, 302)
        # url redirection ok?
        self.assertEqual(response.url, "/agenda/#seccion_11")
        # response from form ok?
        self.assertIn("Cancelar", respon.POST["Cancelar"])

    def test_alter_day_view_change_data_form_action(self):
        """
        Simulates User input data in form
        data to save
        """
        view_url = reverse("alter_day", kwargs={"date": self.date})
        self.form = {
            "shift": ["T"],  # Shift is changed by test. Original is "M"
            "overtime": ["0"],
            "keep_day": ["False"],
            "change_payable": ["False"],
            "comments": [""],
        }
        self.client.post(view_url, data=self.form, follow=True)

        # User changes are saved?
        self.assertTrue(AlterDay.objects.filter(date=self.date).exists())

    def test_alter_day_view_restore_button_action(self):
        """
        Simulates Cancelar button press in form
        No accitions, no data to save
        """
        factory = RequestFactory()
        view_url = reverse("alter_day", kwargs={"date": DATE_STR})
        self.form = {
            "shift": ["T"],
            "overtime": ["0"],
            "keep_day": ["False"],
            "change_payable": ["False"],
            "comments": [""],
            "restaurar_dia": ["Restaurar Dia"],  # Button pressed
        }
        response = self.client.post(view_url, data=self.form)

        respon = factory.post(view_url, data=self.form)

        #  Redirection code ok?
        self.assertEqual(response.status_code, 302)
        # url redirection ok?
        self.assertEqual(response.url, "/agenda/#seccion_11")
        # response from form ok?
        self.assertIn("Restaurar Dia", respon.POST["restaurar_dia"])
        # changes are deleted?
        self.assertFalse(AlterDay.objects.filter(date=self.date).exists())


# New funcionality tests, use only in new adds fields or funcionality:
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
                    print(f"Los atributos '{atributo}' son iguales en ambos objetos.")
                    print("TODO CORRECTO")

                else:
                    print(
                        f"Los atributos '{atributo}' no son iguales en ambos objetos."
                    )
                    print(getattr(recap, atributo), "----", getattr(re, atributo))
