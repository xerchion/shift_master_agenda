from datetime import datetime
from typing import Optional

from django.http import HttpRequest
from django.urls import reverse

from ..config.constants import DAY_MODIFIED_OK
from ..forms import AlterDayForm
from ..logic.Day import Day
from ..logic.Schedule import Schedule
from ..models import AlterDay, User
from .UserAdapter import UserAdapter


class AlterDayController:
    def __init__(self, user_id: int, date: str, schedule: Schedule) -> None:
        self.date: datetime = datetime.strptime(date, "%Y-%m-%d")
        self.day: Day = schedule.search_day(self.date)

        self.month_name: str = schedule.months[self.date.month - 1].name
        self.user: User = UserAdapter.get_user(user_id)
        self.day_saved: bool = False
        self.schedule: Schedule = schedule
        self.url_redirection: Optional[str] = None
        self.form: Optional[AlterDayForm] = None
        self.message: Optional[str] = None

    def restart_day(self) -> None:
        """
        Restarts the day by creating a new instance of Day with the same date, shift, and user.
        Deletes any existing saved day for the same date and year.

        """
        # TODO creo que esto no sirve para nada
        # new_day = Day(self.day.date)
        # new_day.shift.primal = self.day.shift.primal
        # new_day.shift_real = self.day.shift.primal

        # Checking if there's a saved day for the same date and year.
        day_saved = AlterDay.objects.filter(
            user=self.user, date=self.day.date, date__year=self.schedule.year
        ).first()

        day_saved.delete() if day_saved else None

    def get_month_number(self) -> str:
        return str(self.date.month)

    def check_if_day_exists(self) -> bool:
        """
        Checks if a day exists in the database.

        """
        self.day_saved = AlterDay.objects.filter(
            user=self.user, date=self.date, date__year=self.schedule.year
        ).first()
        return True if self.day_saved else False

    def save_day(self, form: AlterDayForm) -> None:
        """
        Saves a day in the database.

        Args:
            form: The form containing the day information.
        """
        alter_day = form.save(commit=False)
        alter_day.user = self.user
        alter_day.date = self.date

        if self.is_altered_by_user(self.day, alter_day):
            alter_day.save()
            self.schedule.fill_colors()

    def fill_form(self, form: AlterDayForm) -> AlterDayForm:
        form.fields["shift"].initial = self.day.get_shift()
        form.fields["overtime"].initial = self.day.shift.overtime
        form.fields["keep_day"].initial = self.day.shift.keep_day
        form.fields["change_payable"].initial = self.day.shift.change_payable
        return form

    def control_response(self, request: HttpRequest) -> None:
        """
        Controls the response from a request.

        Args:
            request: The HTTP request object.

        """
        response = request.POST
        month = self.get_month_number()
        self.url_redirection = reverse("agenda") + "#seccion_" + month
        if "restaurar_dia" in response:
            self.restart_day()
        if "Cancelar" in response or "restaurar_dia" in response:
            self.message = "exit"
        else:
            self.form = AlterDayForm(request.POST)
            if self.check_if_day_exists():
                self.form = AlterDayForm(request.POST, instance=self.day_saved)
            if self.form.is_valid():
                self.save_day(self.form)
                self.message = DAY_MODIFIED_OK

    def generate_form(self) -> AlterDayForm:
        """
        Generates a form for altering a day.

        Returns:
            AlterDayForm: The form for altering a day.
        """
        if self.check_if_day_exists():
            form = AlterDayForm(instance=self.day_saved)
        else:
            form = AlterDayForm(instance=self.user)
            form = self.fill_form(form)
        return form

    @classmethod
    def load_alter_days_db(cls, user: User, schedule: Schedule) -> Schedule:
        """
        Loads altered days from the database and updates the schedule.

        Args:
            user (User): The user for whom altered days are loaded.
            schedule (Schedule): The schedule to be updated.

        Returns:
            Schedule: The updated schedule.
        """
        alter_days = AlterDay.objects.filter(user=user, date__year=schedule.year)

        for alter_day in alter_days:
            index_day = alter_day.date.day - 1
            index_month = alter_day.date.month - 1
            day = schedule.months[index_month].days[index_day]
            day = cls.load_day(day, alter_day)

            schedule.months[index_month].days[index_day] = day

        return schedule

    @classmethod
    def load_day(cls, day: Day, alter_day: AlterDay) -> Day:
        """
        Loads altered day information into a Day object.

        Args:
            day (Day): The Day object to be updated with altered information.
            alter_day (AlterDay): The AlterDay object containing altered information.

        Returns:
            Day: The updated Day object.
        """
        day.shift.new = alter_day.shift
        day.shift.overtime = int(alter_day.overtime)
        day.shift.keep_day = alter_day.keep_day
        day.shift.change_payable = alter_day.change_payable
        day.shift_real = alter_day.shift
        day.alter_day = True

        return day

    def is_altered_by_user(self, day: Day, form: AlterDayForm) -> bool:
        """Check if a day has been modified by the user

        Args:
            day (Day): Day to check
            form (Form): Form response

        Returns:
            bool: True if the day has been modified, False otherwise
        """
        form = self.clean_data_form(form)
        if form.shift != day.get_shift():
            return True
        if int(form.overtime) != int(day.shift.overtime):
            return True
        if form.keep_day != day.shift.keep_day:
            return True
        if form.change_payable != day.shift.change_payable:
            return True
        if form.comments != day.comments:
            return True
        return False

    def clean_data_form(self, form: AlterDayForm) -> AlterDayForm:
        """Clear the form of empty or null data

        Args:
            form (Form): Form response

        Returns:
            Form: Cleaned form
        """
        if not form.overtime:
            form.overtime = "0"
        if not form.comments:
            form.comments = ""
        return form
