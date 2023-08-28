from ..config.constants import EVENING, MORNING, NIGHT, SPLIT


class Recap:
    def __init__(self) -> None:
        self.name = ""
        self.number_of_days = 0
        self.mornings = 0
        self.evenings = 0
        self.nights = 0
        self.split_intensive = 0
        self.workings = 0
        self.frees = 0
        self.holidays = 0
        self.extra_holidays = 0
        self.holidays_not_worked = 0
        self.change_payables = 0
        self.keep_days = 0
        self.overtimes = 0
        self.laborals = 0
        self.days_weekend = 0
        self.extra_keep = 0
        self.extra_payed = 0

    @classmethod
    def calculate(cls, data, name):
        recap = Recap()
        recap.name = name
        if type(data) == list:
            for elem in data:
                elem_recap = Recap.calculate(elem, elem.name)
                for attr_name, attr_value in vars(elem_recap).items():
                    print(attr_name, attr_value)
                    if attr_name != "name":
                        current_value = getattr(recap, attr_name, 0)
                        total_value = int(current_value) + int(attr_value)
                        setattr(recap, attr_name, total_value)
        else:
            recap.number_of_days = len(data.days)
            recap.mornings = data.count_shift(MORNING)
            recap.evenings = data.count_shift(EVENING)
            recap.nights = data.count_shift(NIGHT)
            recap.split_intensive = data.count_shift(SPLIT)
            recap.workings = (
                recap.mornings + recap.evenings + recap.nights + recap.split_intensive
            )
            recap.frees = data.count_shift("D")
            recap.holidays = data.count_holidays()
            recap.extra_holidays = data.count_extra_holidays()
            recap.holidays_not_worked = recap.holidays - recap.extra_holidays
            recap.overtimes = data.count_overtimes()
            recap.change_payables = data.count_change_payables()
            recap.keep_days = data.count_change_payables()
            recap.laborals = data.count_laborable_days()
            recap.days_weekend = data.count_weekends_days()
            recap.extra_keep = data.count_extra_keep()
            recap.extra_payed = data.count_extra_payed()

        return recap
