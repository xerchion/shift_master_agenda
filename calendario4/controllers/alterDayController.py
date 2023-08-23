from datetime import datetime

from django.urls import reverse

from ..config.constants import DAY_MODIFIED_OK
from ..controllers.UserAdapter import UserAdapter
from ..forms import AlterDayForm
from ..logic.Day import Day
from ..models import AlterDay


class AlterDayController:
    def __init__(self, user_id, date, schedule) -> None:
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.day = schedule.search_day(self.date)
        self.month_name = schedule.months[self.date.month - 1].name
        self.user = UserAdapter.get_user(self, user_id)
        self.day_saved = False
        self.schedule = schedule
        self.url_redirection = None
        self.form = None
        self.message = None

    def restart_day(self):
        new_day = Day(self.day.date)
        new_day.shift.primal = self.day.shift.primal
        new_day.shift_real = self.day.shift.primal
        day_saved = AlterDay.objects.filter(user=self.user, date=self.day.date).first()
        if day_saved:
            day_saved.delete()
        return

    def get_month_number(self):
        return str(self.date.month)

    def get_date(self):
        return self.day.date

    def filter_response(self, response):
        if "restaurar_dia" in response:
            self.restart_day()
        if "Cancelar" in response or "restaurar_dia" in response:
            return True
        return False

    def exists_day(self):
        """Return True if exists in Database"""
        self.day_saved = AlterDay.objects.filter(user=self.user, date=self.date).first()
        return True if self.day_saved else False

    def save_day(self, form):
        alter_day = form.save(commit=False)
        alter_day.user = self.user
        alter_day.date = self.date
        if self.schedule.set_altered_day(self.day, alter_day):
            alter_day.save()
            self.schedule.update_day(self.day, alter_day)
            self.schedule.fill_colors()

    def fill_form(self, form):
        form.fields["shift"].initial = self.day.shift_real
        form.fields["extra_hours"].initial = self.day.shift.overtime
        form.fields["keep_day"].initial = self.day.shift.keep_day
        form.fields["change_payable"].initial = self.day.shift.change_payable
        return form

    def control_response(self, request):
        response = request.POST
        month = self.get_month_number()
        self.url_redirection = reverse("agenda") + "#seccion_" + month
        if "restaurar_dia" in response:
            self.restart_day()
        if "Cancelar" in response or "restaurar_dia" in response:
            self.message = "exit"
        else:
            self.form = AlterDayForm(request.POST)
            if self.exists_day():
                self.form = AlterDayForm(request.POST, instance=self.day_saved)
            if self.form.is_valid():
                self.save_day(self.form)
                self.message = DAY_MODIFIED_OK

    def without_post(self):
        if self.exists_day():
            form = AlterDayForm(instance=self.day_saved)
        else:
            form = AlterDayForm(instance=self.user)
            form = self.fill_form(form)
        return form
