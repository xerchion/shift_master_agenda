from time import sleep

from colorama import Fore, init

from ..config.constants import (EVENING, EXTRA_HOLIDAY, FREE_DAY, HOLIDAY,
                                MORNING, NIGHT, SPLIT)
from ..models import Category, Color, Team


def print_red(message: str) -> None:
    """
    Prints a message in red color.

    Args:
        message (str): The message to be printed.

    """
    # Initializes colorama for Windows systems
    init()
    # Prints message in red
    print(Fore.RED + "-" * 50)
    print(str(message))
    print("-" * 50)
    print(Fore.WHITE)


def create_color_mapping(colors: Color) -> dict:
    """
    Creates a mapping of color values.

    Args:
        colors (Color): An instance of the Color class containing color values.

    Returns:
        dict: A mapping of color constants to their respective values.
    """
    return {
        MORNING: colors.morning,
        EVENING: colors.afternoon,
        NIGHT: colors.night,
        FREE_DAY: colors.free,
        HOLIDAY: colors.holiday,
        EXTRA_HOLIDAY: colors.extra_holiday,
        SPLIT: colors.split_shift,
    }


def init_tables_constants():
    CATEGORY = [
        {"id": 1, "number": 1, "text": "Tácnico Titulado Superior", "precio1": None},
        {"id": 2, "number": 2, "text": "Técnico Titulado Medio", "precio1": None},
        {"id": 3, "number": 3, "text": "Técnico No Titulado", "precio1": None},
        {"id": 4, "number": 4, "text": "Encargado", "precio1": None},
        {"id": 5, "number": 5, "text": "Capataz de turno", "precio1": None},
        {"id": 6, "number": 6, "text": "Almacenero", "precio1": None},
        {"id": 7, "number": 7, "text": "Oficial de 2ª", "precio1": None},
        {"id": 8, "number": 8, "text": "Operario de embotellado", " precio1": None},
        {"id": 9, "number": 9, "text": "Auxiliar", "precio1": None},
        {"id": 10, "number": 10, "text": "Oficial de 3ª", "precio1": None},
    ]
    for cat in CATEGORY:
        cat_id = cat["id"]
        catreg = Category(number=int(cat_id), text=cat["text"], precio1=None)
        catreg.save()
    TEAMS = [
        {"id": 1, "letter": "A", "text": "Turno A", "color": None},
        {"id": 2, "letter": "B", "text": "Turno B", "color": None},
        {"id": 3, "letter": "C", "text": "Turno C", "color": None},
        {"id": 4, "letter": "D", "text": "Turno D", "color": None},
        {"id": 5, "letter": "E", "text": "Turno E", "color": None},
    ]
    for cat in TEAMS:
        catreg = Team(letter=cat["letter"], text=cat["text"], color=None)
        catreg.save()


def pause(message: str, time: float = 0) -> None:
    """
    Prints a message in red and then pauses for a specified amount of time.

    Args:
        message (str): The message to be printed.
        time (float, optional): The duration of the pause in seconds. Defaults to 0.

    Returns:
        None
    """
    print_red(message)
    sleep(time)


# Tests utils.........................
def check_integrity_attrs(object, obj_attrs):
    """Check that the attributes of an object have not changed."""
    result = True
    message = None
    attrs = [
        attr
        for attr in dir(object)
        if not callable(getattr(object, attr)) and not attr.startswith("__")
    ]
    # print(attrs)
    name = type(object).__name__
    message = "La integridad de: " + name + "ha cambiado"
    if attrs != obj_attrs:
        result = False
        message = message
    return result, message
