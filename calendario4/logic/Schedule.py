from calendar import monthrange
from datetime import date, timedelta

import holidays

from ..config.constants import NONE_DAY
from ..models import AlterDay
from .Day import Day
from .Month import Month
from .Pattern import Pattern
from .Recap import Recap
from .Week import Week


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
        self.__fill_with_holydays()
        self.__update_schedule()
        self.__fill_with_colors()

    def __create(self):
        self.months = Month.create_months_struct(self)
        actual_day = date(self.year, 1, 1)
        cont = 0
        for i, month in enumerate(self.months):
            self.months[i] = Month(i + 1)
            cont += 1
            last_month_day = monthrange(self.year, i + 1)[1]
            cont2 = 0
            for day in range(0, last_month_day):
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

    def create_weeks(self):
        def calculate_weeks_month(month):
            number = 0
            for day in month.days:
                if day.number == 1 and day.name != "Lunes":
                    number += 1
                if day.name == "Lunes":
                    number += 1
            return number

        def create_weeks_struct(total):
            assert type(total).__name__ == "int", (
                "El tipo no es correcto :"
                + type(total).__name__
                + "Deberia ser un entero"
            )
            weeks = []
            for _ in range(total):
                weeks.append(Week(0))
            for i, week in enumerate(weeks):
                print("Semana: ", i)
                for day in range(7):
                    weeks[i].days.append(Day(date(2000, 1, 1)))
            assert len(weeks) == total, (
                "la cantidad de semanas no corresponde."
                + "salen: "
                + str(len(weeks))
                + ", pero deberian ser:"
                + str(total)
            )
            return weeks

        for i, month in enumerate(self.months):
            weeks_on_month = calculate_weeks_month(month)
            self.months[i].weeks = create_weeks_struct(weeks_on_month)

            day = self.months[i].days[0]
            date_actual_day = day.date
            count = 0
            week_count = 0
            while date_actual_day.month == i + 1:
                if date_actual_day.day == 1:
                    count_for = 0
                    for x in range(0, date_actual_day.weekday()):
                        count_for += 1
                    assert count_for == date_actual_day.weekday(), "mal"
                date_data = Day(date(2000, 1, 1))
                self.months[i].weeks[week_count].days.append(date_data)

                count += 1
                date_actual_day += timedelta(days=1)
            tam = len(self.months[i].days)
            assert count == tam, "El tamaño no corresponde "

    def create_spaces(self):
        for i, month in enumerate(self.months):
            self.months_view.append(Month(i + 1))
            init_days = []
            last_days = []
            first_day = month.days[0]
            for j in range(first_day.date.weekday()):
                init_days.append(Day(NONE_DAY))
                init_days[-1].date = None
            final_day = month.days[-1]
            for k in range(final_day.date.weekday(), 6):
                last_days.append(Day(NONE_DAY))
                last_days[-1].date = None
            between_days = self.months[i].days

            self.months_view[i].days = init_days + between_days + last_days

            tam = len(self.months_view[i].days)
            tam_sum = len(init_days) + len(between_days) + len(last_days)

            assert tam == tam_sum, "La suma no corresponde"

    def __fill_with_colors(self):
        for month in self.months:
            for day in month.days:
                day.aply_color(self.colors)

    def fill_colors(self):
        self.__fill_with_colors()

    def __fill_with_holydays(self):
        year = self.year
        # From Spain
        for i in holidays.Spain(years=year).items():
            mesFestivo = i[0].month
            diaFestivo = i[0].day

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
        self.months[5].days[0].holiday = True

    def __update_schedule(self):
        for month in self.months:
            for day in month.days:
                if day.shift.changed:
                    day.shift_real = day.shift.new
                else:
                    day.shift_real = day.shift.primal

                if day.shift_real in ["M", "T", "N", "P"]:
                    day.working = True

    def search_day(self, date):
        month = date.month
        day = date.day
        return self.months[month - 1].days[day - 1]

    def set_altered_day(self, day, form):
        form = self.clean_data_form(form)
        if form.shift != day.shift_real:
            return True
        if int(form.extra_hours) != int(day.shift.overtime):
            return True
        if form.keep_day != day.shift.keep_day:
            return True
        if form.change_payable != day.shift.change_payable:
            return True
        if form.comments != day.comments:
            return True
        return False

    def clean_data_form(self, form):
        if not form.extra_hours:
            form.extra_hours = "0"
        if not form.comments:
            form.comments = ""
        return form

    def update_day(self, day, form):
        num_month = day.date.month - 1
        num_day = day.date.day - 1
        update_day = day
        if form.shift != day.shift_real:
            update_day.shift.changed = True
            update_day.shift.new = form.shift
            update_day.shift_real = form.shift
            self.__fill_with_colors()

        update_day.shift.overtime = form.extra_hours
        update_day.shift.keep_day = form.keep_day
        update_day.shift.change_payable = form.change_payable

        self.months[num_month].days[num_day] = update_day

    def load_alter_days_db(self, user):
        alter_days = AlterDay.objects.filter(user=user)

        for alter_day in alter_days:
            n_day = alter_day.date.day - 1
            n_month = alter_day.date.month - 1

            day = self.months[n_month].days[n_day]

            day.shift_real = alter_day.shift
            day.shift.extra_hours = alter_day.extra_hours
            day.shift.keep_day = alter_day.keep_day
            day.shift.change_payable = alter_day.change_payable
            day.alter_day = True

            self.months[n_month].days[n_day] = day

        self.__fill_with_colors()

    def calculate_recap_year(self):
        recap = Recap()
        recap.name = self.year
        for month in self.months:
            recap_month = month.calculate_recap()
            for attr_name, attr_value in vars(recap_month).items():
                if attr_name != "name":
                    current_value = getattr(recap, attr_name, 0)
                    total_value = int(current_value) + int(attr_value)
                    setattr(recap, attr_name, total_value)
        return recap
