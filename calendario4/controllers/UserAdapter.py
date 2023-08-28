from django.contrib.auth.models import User

from ..config.constants import (BASE_DAY_COLORS, EVENING, EXTRA_HOLIDAY,
                                FREE_DAY, HOLIDAY, MORNING, NIGHT, SPLIT)
from ..controllers.utils import parse_colors
from ..models import Color, MyUser


class UserAdapter:
    def __init__(self, id=None) -> None:
        self.id = id
        if id:
            self.user = User.objects.get(id=id)
            self.my_user = MyUser.objects.get(user=self.user)
        else:
            self.user = None

    def add_new_user(self, name, pswd, team):
        new_user = User.objects.create_user(username=name, password=pswd)
        new_user.save()
        self.user = new_user

        new_my_user = MyUser(user_name=name, user=new_user, team=team)
        new_my_user.save()
        self.my_user = new_my_user

        self.apply_default_colors()

        return UserAdapter(new_user.id)

    def check_user(self, id):
        is_in_auth = User.objects.filter(id=id).exists()
        is_in_custom = MyUser.objects.filter(user=id).exists()
        return is_in_auth and is_in_custom

    def see_user(self, id):
        # ver los datos del usuario en ambas tablas.
        user = self.get_user(id)
        print("Datos de la tabla Auth_user:")
        print("Username:", user.username, "Códico id: ", user.id)

        print("..........................................................")

        user = MyUser.objects.get(user=id)
        print("Datos de la tabla MyUser:")
        print("Username:", user.user_name, "Códico id: ", user.user)

    def create_new_my_user(self, name, password):
        return MyUser(user_name=name, password=password)

    @classmethod
    def get_user(cls, id):
        return User.objects.get(id=id)

    def get_my_user(self):
        return MyUser.objects.get(user=self.id)

    def apply_default_colors(self):
        if self.exists(self.id):
            color_obj = Color.objects.get(user=self.user)
        else:
            color_obj = Color(user=self.user)

        color_obj.morning = BASE_DAY_COLORS[MORNING]
        color_obj.afternoon = BASE_DAY_COLORS[EVENING]
        color_obj.night = BASE_DAY_COLORS[NIGHT]
        color_obj.split_shift = BASE_DAY_COLORS[SPLIT]
        color_obj.free = BASE_DAY_COLORS[FREE_DAY]
        color_obj.holiday = BASE_DAY_COLORS[HOLIDAY]
        color_obj.extra_holiday = BASE_DAY_COLORS[EXTRA_HOLIDAY]
        color_obj.save()

    def exists(self, data):
        if type(data) == int:
            return User.objects.filter(id=data).exists()
        elif type(data) == str:
            return User.objects.filter(username=data).exists()

    def get_colors(self):
        return parse_colors(Color.objects.get(user=self.id))

    def get_team(self):
        return self.my_user.team

    @classmethod
    @property
    def team(cls):
        return MyUser.objects.get(user=id).team
