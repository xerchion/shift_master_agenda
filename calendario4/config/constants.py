from datetime import date

SHIFT_STRING_ES = ["Mañana", "Tarde", "Noche", "Descanso", "Intensiva/Partida"]

# Shift
KINDS_SHIFTS = ["M", "T", "N", "D", "P"]
KINDS_SHIFTS_STRING = SHIFT_STRING_ES
SHIFTS = tuple(zip(KINDS_SHIFTS, KINDS_SHIFTS_STRING))
FREE_DAY = "D"

KINDS_SHIFTS_STRING = SHIFT_STRING_ES
SHIFTS = tuple(zip(KINDS_SHIFTS, KINDS_SHIFTS_STRING))
FREE_DAY = "D"

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
NAME_USER_EXISTS = "Ya existe un usuario con ese nombre"
USER_SIGNUP_OK = "Usuario dado de alta con exito"

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
    {"id": 1, "number": 1, "text": "Técnico Titulado Superior",
     "precio1": None},
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
    "M": "#5DADE2",
    "T": "#F5B041",
    "N": "#000000",
    "D": "#7F8C8D",
    "F": "#F1948A",
    "E": "#FA1D04",
    "P": "#A9DFBF",
}
