from django.contrib.auth.models import User

from ..config.constants import BASE_DAY_COLORS
from ..models import Color, MyUser


class UserAdapter:
    def __init__(self) -> None:
        self.user = ""

    def add_new_user(self, name, pswd):
        new_user = User.objects.create_user(username=name, password=pswd)
        new_user.save()

        new_myuser = MyUser(user_name=name, user=new_user)
        self.apply_default_colors(new_user)

        new_myuser.save()
        return new_user

    def check_user(self, id):
        is_in_auth = User.objects.filter(id=id).exists()
        is_in_custom = MyUser.objects.filter(user=id).exists()
        return is_in_auth and is_in_custom

    def see_user(self, id):
        # ver los datos del usuario en ambas tablas.
        user = User.objects.get(id=id)
        print("Datos de la tabla Auth_user:")
        print("Username:", user.username, "Códico id: ", user.id)

        print("..........................................................")

        user = MyUser.objects.get(user=id)
        print("Datos de la tabla MyUser:")
        print("Username:", user.user_name, "Códico id: ", user.user)

    def create_new_my_user(self, name, password):
        return MyUser(user_name=name, password=password)

    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    def get_my_user(self, user_id):
        user = self.get_user(user_id)
        return MyUser.objects.get(user=user)

    def apply_default_colors(self, my_user):
        color_obj = Color(user=my_user)

        # Rellenar los campos con los valores del diccionario BASICS
        color_obj.morning = BASE_DAY_COLORS["M"]
        color_obj.afternoon = BASE_DAY_COLORS["T"]
        color_obj.night = BASE_DAY_COLORS["N"]
        color_obj.split_shift = BASE_DAY_COLORS["P"]
        color_obj.free = BASE_DAY_COLORS["D"]
        color_obj.holiday = BASE_DAY_COLORS["F"]
        color_obj.extra_holiday = BASE_DAY_COLORS["E"]

        color_obj.save()

    def restart_colors(self, my_user):
        colours = Color.objects.filter(id=my_user.id).first()
        if colours:
            colours.morning = BASE_DAY_COLORS["M"]
            colours.afternoon = BASE_DAY_COLORS["T"]
            colours.night = BASE_DAY_COLORS["N"]
            colours.split_shift = BASE_DAY_COLORS["P"]
            colours.free = BASE_DAY_COLORS["D"]
            colours.holiday = BASE_DAY_COLORS["F"]
            colours.extra_holiday = BASE_DAY_COLORS["E"]

            colours.save()
        return

    def exists(self, name):
        return User.objects.filter(username=name).exists()
