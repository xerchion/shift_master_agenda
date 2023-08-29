import holidays

from ..config.constants import FIRST
from .Month import Month
from .Pattern import Pattern


class Schedule:
    def __init__(self, year, team, colors):
        self.year = year
        self.team = team
        self.months = []
        self.months_view = []
        self.colors = colors

        self.__create()
        self.__fill_with_pattern()
        self.create_spaces_view()
        self.fill_holydays()
        self.fill_colors()

    def __create(self):
        self.months = Month.create_months_struct(self, self.year)

    def __fill_with_pattern(self):
        pattern = Pattern(self.year, self.team)
        i = 0
        for month in self.months:
            final = i + month.days_number
            month.fill_day_shifts(pattern.pattern[i: final + 1])
            i = final

    def create_spaces_view(self):
        for i, month in enumerate(self.months):
            self.months_view.append(Month(i + 1))
            month_view = month.create_month_spaces(self.months_view[i])
            self.months_view[i] = month_view

    def fill_holydays(self):
        year = self.year
        # From Spain
        for i in holidays.Spain(years=year).items():
            holiday_month = i[FIRST].month
            holiday_day = i[FIRST].day
            self.months[holiday_month - 1].aply_holiday(holiday_day - 1)

            # self.months[mesFestivo - 1].days[diaFestivo - 1].holiday = True
        # From loja
        #   25 de Abril Dia de San Marcos
        self.months[3].aply_holiday(24)
        #   15 de agosto  Asunción de la Virgen.
        self.months[7].aply_holiday(14)
        #   29 de agosto  Feria de Loja.
        self.months[7].aply_holiday(28)
        #   28 de febrero dia de andalucia
        self.months[1].aply_holiday(27)
        # 1 DE MAYO DIAaply_holiday(28)
        self.months[4].aply_holiday(FIRST)

    def fill_colors(self):
        for month in self.months:
            month.aply_colors(self.colors)

    def search_day(self, sdate):
        month = self.months[sdate.month - 1]
        return month.extract_day(sdate.day)

    # TODO esta funcion deberia ser de day o bien del controller AlterDayControler
    def set_altered_day(self, day, form):
        """Check if a day has been modified by the user

        Args:
            day (Day): day to check
            form (Form): Form response

        Returns:
            Boolean
        """
        form = self.clean_data_form(form)
        if form.shift != day.get_shift():
            return True
        if int(form.overtime) != int(day.shift.overtime):
            return True
        if form.keep_day != day.shift.keep_day:
            return True
        if form.change_payable != day.shift.change_payable:
            return True
        if form.comments != day.comments:
            return True
        return False

    def clean_data_form(self, form):
        """Clear the form of empty or null data

        Args:
            form (Form): Form response

        Returns:
            Form: cleaned
        """
        if not form.overtime:
            form.overtime = "0"
        if not form.comments:
            form.comments = ""
        return form

    def calculate_recap_year(self):
        all_months = []
        for month in self.months:
            month.calculate_recap()
            all_months.append(month.recap)
        total_recap = type(all_months[0])()
        for recap in all_months:
            for attr_name, attr_value in vars(recap).items():
                if attr_name != "name":
                    current_value = getattr(total_recap, attr_name, 0)
                    total_value = int(current_value) + int(attr_value)
                    setattr(total_recap, attr_name, total_value)

        total_recap.name = self.year
        return total_recap
