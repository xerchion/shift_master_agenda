from ..config.constants import KINDS_SHIFTS, WEEK_DAYS
from .Shift import Shift


class Day:
    def __init__(self, date):
        date_type = type(date).__name__
        assert date_type == "date", (
            "El tipo es incorrecto, debe ser date, pero es: " + date_type
        )
        self.date = date
        self.name = self.say_your_name()
        self.number = date.day
        self.holiday = False
        self.shift = Shift("D")
        self.shift_real = self.shift.primal
        self.working = False
        self.colour = ""
        self.alter_day = False
        self.comments = ""

    # TODO SIN APLICAR, USALO Y AÑADE A RECAPS
    def set_shift_change(self, new_shift, payed=False):
        assert new_shift in KINDS_SHIFTS and payed is False or payed
        self.shift.set_shift_change(new_shift, payed)

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

    def is_holiday(self):
        return self.holiday

    def is_change_payable(self):
        return self.shift.change_payable

    def say_your_name(self):
        return WEEK_DAYS[self.date.weekday()]

    def aply_color(self, colors):
        self.colour = colors[self.shift_real]

        if self.holiday:
            self.colour = colors["F"]
        if self.holiday and self.working:
            self.colour = colors["E"]
