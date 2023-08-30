from datetime import date

SHIFT_STRING_ES = ["Mañana", "Tarde", "Noche", "Descanso", "Intensiva/Partida"]

# Shift
MORNING = "M"
EVENING = "T"
NIGHT = "N"
SPLIT = "P"
FREE_DAY = "D"
HOLIDAY = "F"
EXTRA_HOLIDAY = "E"

KINDS_SHIFTS = [MORNING, EVENING, NIGHT, FREE_DAY, SPLIT]
WORK_DAYS = [shift for shift in KINDS_SHIFTS if shift != FREE_DAY]
KINDS_SHIFTS_STRING = SHIFT_STRING_ES
SHIFTS = tuple(zip(KINDS_SHIFTS, KINDS_SHIFTS_STRING))


KINDS_SHIFTS_STRING = SHIFT_STRING_ES
SHIFTS = tuple(zip(KINDS_SHIFTS, KINDS_SHIFTS_STRING))

# Pattern
INITIAL_YEAR = 2022
FIXED_SERIE_AMOUNT_DAYS = [2, 2, 3, 4, 3, 2, 2, 5, 2, 3, 2, 5]
TEAM_VALUES_SERIE = KINDS_SHIFTS[:4] * 3
TEAM_POSITION_DAYS = {"A": 19, "B": 33, "C": 12, "D": 26, "E": 5}

# AlterDay Constants
DAY_MODIFIED_OK = "Dia modificado con exito"

# signUpController
PASSWORDS_NOT_MATCH = "La contraseña no coincide al repetirla, \
                       por favor intentalo de nuevo."
NAME_USER_EXISTS = "Ya existe un usuario con ese nombre, elige otro."
USER_SIGNUP_OK = "Usuario dado de alta con exito."
FORM_NOT_VALID = "Datos introducidos incorrectos."
NECESSARY_TEAM = "La elección del Turno es obligatoria."

# Day
WEEK_DAYS = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
]

WEEK_DAYS_LETTER = ["L", "M", "X", "J", "V", "S", "D"]
NONE_DAY = date(2000, 1, 1)

# Teams
# Initial data to DB
TEAMS_INITIAL = [
    {"id": 1, "letter": "A", "text": "Turno A", "color": None},
    {"id": 2, "letter": "B", "text": "Turno B", "color": None},
    {"id": 3, "letter": "C", "text": "Turno C", "color": None},
    {"id": 4, "letter": "D", "text": "Turno D", "color": None},
    {"id": 5, "letter": "E", "text": "Turno E", "color": None},
]

# ["A", "B", "C", "D", "E]
TEAMS_LIST = [team["letter"] for team in TEAMS_INITIAL]

# Categories
# Initial data to DB
CATEGORY = [
    {"id": 1, "number": 1, "text": "Técnico Titulado Superior", "precio1": None},
    {"id": 2, "number": 2, "text": "Técnico Titulado Medio", "precio1": None},
    {"id": 3, "number": 3, "text": "Técnico No Titulado", "precio1": None},
    {"id": 4, "number": 4, "text": "Encargado", "precio1": None},
    {"id": 5, "number": 5, "text": "Capataz de turno", "precio1": None},
    {"id": 6, "number": 6, "text": "Almacenero", "precio1": None},
    {"id": 7, "number": 7, "text": "Oficial de 2ª", "precio1": None},
    {"id": 8, "number": 8, "text": "Operario de embotellado", "precio1": None},
    {"id": 9, "number": 9, "text": "Auxiliar", "precio1": None},
    {"id": 10, "number": 10, "text": "Oficial de 3ª", "precio1": None},
]


BASE_DAY_COLORS = {
    MORNING: "#5DADE2",
    EVENING: "#F5B041",
    NIGHT: "#000000",
    FREE_DAY: "#7F8C8D",
    HOLIDAY: "#F1948A",
    EXTRA_HOLIDAY: "#FA1D04",
    SPLIT: "#A9DFBF",
}
FIRST = 0
LAST = -1
