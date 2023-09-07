from ..config.constants import FREE_DAY, KINDS_SHIFTS


class Shift:
    def __init__(self, name):
        assert name in KINDS_SHIFTS
        self.primal = name
        self.new = None
        self.change_payable = False
        self.overtime = 0
        self.keep_day = False

    def is_free(self):
        compare_new = self.new == FREE_DAY
        compare_primal = self.primal == FREE_DAY
        return compare_new if self.new else compare_primal
