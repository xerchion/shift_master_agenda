from ..config.constants import KINDS_SHIFTS, FREE_DAY


class Shift:
    def __init__(self, name):
        assert name in KINDS_SHIFTS
        self.primal = name
        self.new = None
        self.changed = False
        self.change_payable = False
        self.overtime = 0
        self.keep_day = False

    # TODO, SIN USAR, HAZLO
    def set_shift_change(self, new, payed=False):
        assert new in self.KINDS_SHIFTS
        self.new = new
        self.changed = True
        if payed:
            self.change_payable = True

    # TODO, SIN USAR, HAZLO
    def is_extra(self):
        return self.primal == self.FREE_DAY and self.new != self.FREE_DAY

    def is_free(self):
        compare_new = self.new == FREE_DAY
        compare_primal = self.primal == FREE_DAY
        return compare_new if self.new else compare_primal
