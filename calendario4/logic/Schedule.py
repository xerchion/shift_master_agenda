from calendar import monthrange
from datetime import date, timedelta

import holidays

from ..config.constants import FIRST, LAST, NONE_DAY
from ..models import AlterDay
from .Day import Day
from .Month import Month
from .Pattern import Pattern
from .Recap import Recap


class Schedule:
    def __init__(self, year, team, colors):
        self.year = year
        self.team = team
        self.months = []
        self.months_view = []
        self.colors = colors

        self.__create()
        self.__fill_with_pattern()
        self.create_spaces()
        self.fill_holydays()
        self.fill_colors()

    def __create(self):
        self.months = Month.create_months_struct(self)
        actual_day = date(self.year, 1, 1)
        cont = 0
        for i, month in enumerate(self.months):
            self.months[i] = Month(i + 1)
            cont += 1
            last_month_day = monthrange(self.year, i + 1)[1]
            cont2 = 0
            for _ in range(0, last_month_day):
                cont2 += 1
                self.months[i].days.append(Day(actual_day))
                actual_day += timedelta(days=1)

    def __fill_with_pattern(self):
        pattern = Pattern(self.year, self.team)
        i = 0
        for month in self.months:
            for day in month.days:
                day.shift.primal = pattern.pattern[i]
                i += 1

    def create_spaces(self):
        for i, month in enumerate(self.months):
            self.months_view.append(Month(i + 1))
            init_days = []
            last_days = []
            first_day = month.days[FIRST]
            for j in range(first_day.date.weekday()):
                init_days.append(Day(NONE_DAY))
                init_days[LAST].date = None
            final_day = month.days[LAST]
            for k in range(final_day.date.weekday(), 6):
                last_days.append(Day(NONE_DAY))
                last_days[LAST].date = None
            between_days = self.months[i].days

            self.months_view[i].days = init_days + between_days + last_days

            tam = len(self.months_view[i].days)
            tam_sum = len(init_days) + len(between_days) + len(last_days)

            assert tam == tam_sum, "La suma no corresponde"

    def fill_colors(self):
        for month in self.months:
            for day in month.days:
                day.aply_color(self.colors)

    def fill_holydays(self):
        year = self.year
        # From Spain
        for i in holidays.Spain(years=year).items():
            mesFestivo = i[FIRST].month
            diaFestivo = i[FIRST].day

            self.months[mesFestivo - 1].days[diaFestivo - 1].holiday = True
        # From loja
        #   25 de Abril Dia de San Marcos
        self.months[4].days[24].holiday = True
        #   15 de agosto  Asunción de la Virgen.
        self.months[8].days[14].holiday = True
        #   29 de agosto  Feria de Loja.
        self.months[8].days[28].holiday = True
        #   28 de febrero dia de andalucia
        self.months[2].days[27].holiday = True
        # 1 DE MAYO DIA DEL TRABAJADOR
        self.months[5].days[FIRST].holiday = True

    def search_day(self, date):
        month = date.month
        day = date.day
        return self.months[month - 1].days[day - 1]

    def set_altered_day(self, day, form):
        """Check if a day has been modified by the user

        Args:
            day (Day): day to check
            form (Form): Form response

        Returns:
            Boolean
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

    def clean_data_form(self, form):
        """Clear the form of empty or null data

        Args:
            form (Form): Form response

        Returns:
            Form: cleaned
        """
        if not form.overtime:
            form.overtime = "0"
        if not form.comments:
            form.comments = ""
        return form

    def load_alter_days_db(self, user):
        alter_days = AlterDay.objects.filter(user=user)

        for alter_day in alter_days:
            n_day = alter_day.date.day - 1
            n_month = alter_day.date.month - 1

            day = self.months[n_month].days[n_day]

            day.shift.new = alter_day.shift
            day.shift.overtime = int(alter_day.overtime)
            day.shift.keep_day = alter_day.keep_day
            day.shift.change_payable = alter_day.change_payable
            day.alter_day = True
            day.shift_real = alter_day.shift

            self.months[n_month].days[n_day] = day

        self.fill_colors()

    def calculate_recap_year(self):
        recap = Recap()
        recap.name = self.year
        for month in self.months:
            recap_month = month.create_recap()
            for attr_name, attr_value in vars(recap_month).items():
                if attr_name != "name":
                    current_value = getattr(recap, attr_name, 0)
                    total_value = int(current_value) + int(attr_value)
                    setattr(recap, attr_name, total_value)
        return recap
