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

    def count_extra_keep(self):
        return sum(1 for day in self.days if day.shift.keep_day)

    def count_extra_payed(self):
        result = 0
        for day in self.days:
            if day.is_extra_payable_day():
                result += 1
                print(day.date, day.shift.primal, day.shift.new)
        return result

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
        result.split_intensive = self.count_shift("P")
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
