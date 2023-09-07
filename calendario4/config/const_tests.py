import calendar
from datetime import datetime

# Schedule's mocks________________________________________________
#  Pattern
SLICE_SIZE = 7
START_PATTERN = ["T", "N", "N", "D", "D", "D", "D"]
END_PATTERN = ["M", "M", "T", "T", "N", "N", "N"]
YEAR = 2023
DATE_STR = "2023-11-8"
DATE_TEST = datetime.strptime(DATE_STR, "%Y-%m-%d")
MONTH = DATE_TEST.month
MONTH_INDEX = MONTH - 1
DAYS_IN_MONTH = calendar.monthrange(YEAR, MONTH)[1]
DAY = DATE_TEST.day
DAY_INDEX = DAY - 1

MONTH_TEST = MONTH - 1
TEAM = "C"
SCHEDULE_ATTRS = ["colors", "months", "months_view", "team", "year"]
MONTH_ATTRS = [
    "days",
    "days_number",
    "name",
    "number",
    "recap",
    "weeks",
]
DAY_ATTRS = [
    "alter_day",
    "colour",
    "comments",
    "date",
    "holiday",
    "name",
    "number",
    "shift",
    "shift_real",
]
SHIFT_ATTRS = [
    "change_payable",
    "keep_day",
    "new",
    "overtime",
    "primal",
]


# Recap's mocks________________________________________________
# 2023 Base, whithout alterd days
RECAP_BASE_YEAR = {
    "name": 2023,
    "number_of_days": 365,
    "mornings": 72,
    "evenings": 73,
    "nights": 75,
    "workings": 220,
    "frees": 145,
    "holidays": 13,
    "extra_holidays": 6,
    "holidays_not_worked": 7,
    "change_payables": 0,
    "keep_days": 0,
    "overtimes": 0,
    "laborals": 260,
    "days_weekend": 105,
    "extra_keep": 0,
    "extra_payed": 0,
}

# 2023 November Team C Base, whithout altered days
RECAP_BASE_MONTH = {
    "name": "Noviembre",
    "number_of_days": 30,
    "mornings": 4,
    "evenings": 5,
    "nights": 7,
    "workings": 16,
    "frees": 14,
    "holidays": 1,
    "extra_holidays": 1,
    "holidays_not_worked": 0,
    "change_payables": 0,
    "keep_days": 0,
    "overtimes": 0,
    "laborals": 22,
    "days_weekend": 8,
}
# MOCKS to:  test_alter_day_recap

DATE_TEST = datetime.strptime(DATE_STR, "%Y-%m-%d")

# Models's mocks________________________________________________
USERNAME = "ejemplo"
PASSWORD = "contraseña123"
MODELS = {
    "LogEntry": 8,
    "Permission": 4,
    "Group": 2,
    "User": 11,
    "ContentType": 3,
    "Session": 3,
    "Team": 4,
    "Category": 4,
    "MyUser": 8,
    "Color": 9,
    "AlterDay": 8,
}

VIEWS_WITHOUT_LOGIN = {
    # Key: view name
    # Value: text to search in the view
    "home": "Bienvenido",
    "signup": "Registro de Nuevo Usuario",
}
VIEWS_WITH_LOGIN = {
    # Key: view name
    # Values: text to search in the view
    "agenda": "Calendario",
    "config": "Datos Personales",
    "recap_year": "Resumen de",
    "signup": "Registro de Nuevo Usuario",
    "change_pass": "Cambio de contraseña",
    "change_color_days": "Cambio de Colores",
}
HTTP_OK = 200


RECAP_ATTRS = [
    "change_payables",
    "days_weekend",
    "evenings",
    "extra_holidays",
    "extra_keep",
    "extra_payed",
    "frees",
    "holidays",
    "holidays_not_worked",
    "keep_days",
    "laborals",
    "mornings",
    "name",
    "nights",
    "number_of_days",
    "overtimes",
    "split_intensive",
    "workings",
]
