import calendar
import locale

from .Recap import Recap


class Month:
    def __init__(self, number):
        self.number = number
        self.name = self.say_your_name()
        self.days = []
        self.weeks = []

    def create_months_struct(self):
        months = []
        while len(months) < 12:
            months.append(Month(1))
        assert_comment = "Num incorrecto de meses: " + str(len(months))
        assert len(months) == 12, assert_comment
        return months
# no Usado

    def fill_day_shifts(self, pattern):
        for day in self.days:
            day.shift.primal = pattern.__next__()

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

    def say_your_name(self):
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        return calendar.month_name[self.number].capitalize()

    def create_recap(self):
        result = Recap()
        result.name = self.name
        result.number_of_days = len(self.days)
        result.mornings = self.count_shift("M")
        result.evenings = self.count_shift("T")
        result.nights = self.count_shift("N")
        result.workings = result.mornings + result.evenings + result.nights
        result.frees = self.count_shift("D")
        result.holidays = self.count_holidays()
        result.extra_holidays = self.count_extra_holidays()
        result.holidays_not_worked = result.holidays - result.extra_holidays
        result.overtimes = self.count_overtimes()
        result.change_payables = self.count_change_payables()
        result.keep_days = self.count_change_payables()
        result.laborals = self.count_laborable_days()
        result.days_weekend = self.count_weekends_days()
        return result

    # Esta puede borrarse, ya tengo hecha la de arriba y COMPROBADA
    def calculate_recap(self):
        result = Recap()
        for day in self.days:
            result.name = self.name
            result.number_of_days = len(self.days)
            result.mornings += 1 if day.shift_real == "M" else 0
            result.evenings += 1 if day.shift_real == "T" else 0
            result.nights += 1 if day.shift_real == "N" else 0
            result.workings = result.mornings + result.evenings + result.nights
            result.frees += 1 if day.shift_real == "D" else 0
            result.holidays += 1 if day.holiday else 0
            result.extra_holidays += 1 if day.holiday and day.working else 0
            result.holidays_not_worked = result.holidays - result.extra_holidays
            result.overtimes += day.shift.overtime
            result.change_payables += 1 if day.shift.change_payable else 0
            result.keep_days += 1 if day.shift.keep_day else 0

            result.laborals += 1 if day.is_laboral() else 0
            result.days_weekend += 1 if day.is_weekend() else 0
        return result
