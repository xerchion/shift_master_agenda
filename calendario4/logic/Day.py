from ..config.constants import (EXTRA_HOLIDAY, FREE_DAY, HOLIDAY, KINDS_SHIFTS,
                                WEEK_DAYS, WORK_DAYS)
from .Shift import Shift


class Day:
    def __init__(self, date):
        date_type = type(date).__name__
        assert date_type == "date", (
            "El tipo es incorrecto, debe ser date, pero es: " + date_type
        )
        self.date = date
        self.name = self.say_your_name()
        self.shift_real = FREE_DAY
        self.number = date.day
        self.holiday = False
        self.shift = Shift(FREE_DAY)
        self.colour = ""
        self.alter_day = False
        self.comments = ""

    def __str__(self):
        return (
            f"Fecha : {self.date}\n"
            f"Turno shift_real : {self.shift_real}\n"
            f"Turno primal : {self.shift.primal}\n"
            f"Turno new: {self.shift.new}\n"
            f"Dia keep_day: {self.shift.keep_day}"
        )

    def set_shift(self, shift):
        self.shift.primal = shift
        self.shift_real = shift

    def equal(self, shift):
        assert shift in KINDS_SHIFTS

        result = self.shift.primal == shift
        if self.shift.new:
            result = self.shift.new == shift

        return result

    def is_laboral(self):
        return not self.is_weekend()

    def is_weekend(self):
        return self.date.weekday() >= 5

    def is_extra_holiday(self):
        return self.holiday and not self.shift.is_free()

    def is_extra_payable_day(self):
        return (not self.shift.keep_day) and self.is_extra_day()

    def is_extra_day(self):
        return self.shift.primal == FREE_DAY and self.is_working_day()

    def is_holiday(self):
        return self.holiday

    def is_change_payable(self):
        return self.shift.change_payable

    def say_your_name(self):
        return WEEK_DAYS[self.date.weekday()]

    def set_color(self, colors):
        self.colour = colors[self.get_shift()]

        if self.holiday:
            self.colour = colors[HOLIDAY]
        if self.holiday and self.is_working_day():
            self.colour = colors[EXTRA_HOLIDAY]

    def set_holiday(self):
        self.holiday = True

    def get_shift(self):
        shift = self.shift.new if self.shift.new else self.shift.primal
        return shift

    def is_working_day(self):
        return (
            (self.shift.new in WORK_DAYS)
            if self.shift.new
            else (self.shift.primal in WORK_DAYS)
        )
