import calendar
import locale
from calendar import monthrange
from datetime import date, timedelta

from ..config.constants import (EVENING, FIRST, LAST, MORNING, NIGHT, NONE_DAY,
                                SPLIT)
from .Day import Day
from .Recap import Recap


class Month:
    def __init__(self, number):
        self.number = number
        self.name = self.say_your_name()
        self.days_number = 0
        self.days = []
        self.weeks = []

    def create_months_struct(self, year):
        months = []
        i = len(months)
        while i < 12:
            months.append(Month(i + 1))
            months[i].create_days_struct(date(year, i + 1, 1))
            months[i].days_number = len(months[i].days)
            i += 1
        assert_comment = "Num incorrecto de meses: " + str(len(months))
        assert len(months) == 12, assert_comment
        return months

    def create_days_struct(self, xdate):
        actual_day = xdate
        cont = 0
        cont += 1
        last_month_day = monthrange(xdate.year, xdate.month)[1]
        cont2 = 0
        for _ in range(0, last_month_day):
            cont2 += 1
            self.days.append(Day(actual_day))
            actual_day += timedelta(days=1)

    def fill_day_shifts(self, pattern):
        i = 0
        for day in self.days:
            day.set_shift(pattern[i])
            i += 1
        return

    def create_month_spaces(self):
        init_days = []
        last_days = []
        first_day = self.days[FIRST]
        for j in range(first_day.date.weekday()):
            init_days.append(Day(NONE_DAY))
            init_days[LAST].date = None
        final_day = self.days[LAST]
        for k in range(final_day.date.weekday(), 6):
            last_days.append(Day(NONE_DAY))
            last_days[LAST].date = None
        between_days = self.days
        return init_days + between_days + last_days

    def aply_holiday(self, holiday_day):
        self.days[holiday_day].set_holiday()

    def aply_colors(self, colors):
        for day in self.days:
            day.set_color(colors)

    def count_overtimes(self):
        return sum(day.shift.overtime for day in self.days)

    def count_weekends_days(self):
        return sum(1 for day in self.days if day.is_weekend())

    def count_shift(self, shift):
        return sum(1 for day in self.days if day.equal(shift))

    def count_holidays(self):
        return sum(1 for day in self.days if day.is_holiday())

    def count_extra_holidays(self):
        return sum(1 for day in self.days if day.is_extra_holiday())

    def count_workable_days(self):
        return sum(1 for day in self.days if day.is_working())

    def count_laborable_days(self):
        return sum(1 for day in self.days if day.is_laboral())

    def count_change_payables(self):
        return sum(1 for day in self.days if day.is_change_payable())

    def count_extra_keep(self):
        return sum(1 for day in self.days if day.shift.keep_day)

    def count_extra_payed(self):
        result = 0
        for day in self.days:
            if day.is_extra_payable_day():
                result += 1
        return result

    def say_your_name(self):
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        return calendar.month_name[self.number].capitalize()

    def create_recap(self):
        result = Recap()
        result.name = self.name
        result.number_of_days = len(self.days)
        result.mornings = self.count_shift(MORNING)
        result.evenings = self.count_shift(EVENING)
        result.nights = self.count_shift(NIGHT)
        result.split_intensive = self.count_shift(SPLIT)
        result.workings = (
            result.mornings + result.evenings + result.nights + result.split_intensive
        )
        result.frees = self.count_shift("D")
        result.holidays = self.count_holidays()
        result.extra_holidays = self.count_extra_holidays()
        result.holidays_not_worked = result.holidays - result.extra_holidays
        result.overtimes = self.count_overtimes()
        result.change_payables = self.count_change_payables()
        result.keep_days = self.count_change_payables()
        result.laborals = self.count_laborable_days()
        result.days_weekend = self.count_weekends_days()
        result.extra_keep = self.count_extra_keep()
        result.extra_payed = self.count_extra_payed()

        return result
