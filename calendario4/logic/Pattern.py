from calendar import isleap

from ..config.constants import (FIXED_SERIE_AMOUNT_DAYS, INITIAL_YEAR,
                                TEAM_POSITION_DAYS, TEAM_VALUES_SERIE,
                                TEAMS_LIST)


class Pattern:
    def __init__(self, year, team):
        assert team in TEAMS_LIST and year >= INITIAL_YEAR
        self.year = year
        self.team = team
        self.pattern = self.__create()

    def __create(self):
        extended_shift_serie = self.__extend_shift_serie(self.year)
        start_day, end_day = self.__calculate_range_period()
        return extended_shift_serie[start_day:end_day]

    def __extend_shift_serie(self, year):
        extended_shift_serie = []
        days = 0
        serie_end = 366 + (year - INITIAL_YEAR) * 366 + 100
        while days < serie_end:
            for i_value in range(0, len(TEAM_VALUES_SERIE)):
                for _ in range(0, FIXED_SERIE_AMOUNT_DAYS[i_value]):
                    extended_shift_serie.append(TEAM_VALUES_SERIE[i_value])
                    days += 1
        return extended_shift_serie

    def __calculate_range_period(self):
        total_days_period = self.__calculate_total_days(INITIAL_YEAR, self.year)
        start_day = TEAM_POSITION_DAYS[self.team] + total_days_period
        end_day = 366 if isleap(self.year) else 365 + start_day
        return start_day, end_day

    def __calculate_total_days(self, INITIAL_YEAR, year):
        total_days_period = 0
        for i in range(INITIAL_YEAR, year):
            total_days_period += 366 if isleap(i) else 365
        return total_days_period
