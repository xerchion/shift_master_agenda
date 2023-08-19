from ..config.constants import KINDS_SHIFTS


class Shift:
    def __init__(self, name):
        assert name in KINDS_SHIFTS
        self.primal = name
        self.new = None
        self.changed = False
        self.change_payable = False
        self.overtime = 0
        self.keep_day = False

    def set_shift_change(self, new, payed=False):
        assert new in self.KINDS_SHIFTS
        self.new = new
        self.changed = True
        if payed:
            self.change_payable = True

    def set_overtime(self, number, keep=False):
        assert number > 0 and number <= 8
        assert keep or keep is False or keep is None
        self.overtime = number
        self.keep_day = keep

    def is_extra(self):
        return self.primal == self.FREE_DAY and self.new != self.FREE_DAY

    def is_free(self):
        compare_new = self.new == self.__FREE_DAY
        compare_primal = self.primal == self.FREE_DAY
        return compare_new if self.new else compare_primal

    def __shifts_to_dict(self):
        return dict(zip(self.KINDS_SHIFTS, self.KINDS_SHIFTS_STRING))

    def get_shift_to_string(self):
        dic = self.__shifts_to_dict()
        result = dic[self.primal]
        if self.changed:
            result = dic[self.new]
        return result


if __name__ == "__main__":
    prueba = "M"
    turno = Shift(prueba)
    print(prueba, "Da como resultado: ", turno.get_shift_to_string())
    turno = Shift(None)
    print("Prueba de None resultado: ", turno.get_shift_to_string())
    turno.set_overtime(3, True)
    print(turno.get_shift_to_string())
