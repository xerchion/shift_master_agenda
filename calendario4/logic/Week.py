import calendar
import locale

from .Day import Day


class Week:
    def __init__(self, number):
        self.number = number
        self.days = []

    def __create(self, data_month):
        self.days.append(None)
        self.name = self.say_your_name()

        month_days = len(data_month)
        for i in range(1, month_days + 1):
            data_day = self.__extract_data_weeks(data_month)
            self.days.append(Day(data_day[i]))

    def fill_day_shifts(self, pattern):
        for day in self.days[1:]:
            day.shift.primal = pattern.__next__()
            day.shift_real = day.shift.primal

    def __len(self, data_month):
        last_week = data_month[-1]
        return max(day.day for day in last_week)

    def __extract_data_weeks(self, data_month):
        result = []
        for day in data_month:
            result.append(day)
        return result

    def calculate_overtimes(self):
        return sum(day.get_overtimes() for day in self.days)

    def count_weekends_days(self):
        return sum(1 for day in self.days if day.is_weekend())

    def count_shift(self, shift):
        return sum(1 for day in self.days if day.equal(shift))

    def count_extra_holidays(self):
        return sum(1 for day in self.days if day.is_extra_holiday())

    def count_workable_days(self):
        return sum(1 for day in self.days if day.is_working())

    def count_laborable_days(self):
        return sum(1 for day in self.days if day.is_laboral())

    def say_your_name(self):
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        return calendar.month_name[self.number].capitalize()
