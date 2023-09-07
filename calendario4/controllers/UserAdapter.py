import inspect

from django.contrib.auth.models import User

from ..config.constants import (BASE_DAY_COLORS, EVENING, EXTRA_HOLIDAY, FORMS,
                                FREE_DAY, HOLIDAY, MORNING, NIGHT, SPLIT)
from ..controllers.utils import parse_colors
from ..forms import ColorForm, CustomPasswordChangeForm, UserConfigForm
from ..models import Color, MyUser


class UserAdapter:
    def __init__(self, id=None) -> None:
        self.id = id
        if id:
            self.user = User.objects.get(id=id)
            self.my_user = MyUser.objects.get(user=self.user)
            self.colors = Color.objects.get(user=self.id)
            self.color_form = self.get_color_form(self.colors)
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

    def create_new_my_user(self, name, password):
        return MyUser(user_name=name, password=password)

    @classmethod
    def get_user(cls, id):
        return User.objects.get(id=id)

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

    def set_team(self, team):
        self.my_user.team = team

    def get_team(self):
        return self.my_user.team

    @classmethod
    @property
    def team(cls):
        return MyUser.objects.get(user=id).team

    def set_color_form(self, response, instance):
        self.color_form = ColorForm(response, instance=instance)
        return self.color_form

    @property
    def color_saved(self):
        return Color.objects.filter(user=self.user).first()

    def get_color_form(self, instance=None, response=None):
        return (
            ColorForm(instance=instance) if instance else ColorForm(instance=self.user)
        )

    def get_config_form(self, response=None, instance=None):
        if response:
            form = UserConfigForm(response, instance=self.my_user)
        else:
            form = UserConfigForm(instance=self.my_user)
        return form

    def get_pass_form(self, response=None, instance=None):
        if response:
            form = CustomPasswordChangeForm(self.user, response)
        else:
            form = CustomPasswordChangeForm(self.user)
        return form

    def get_form(self, response=None, instance=None):
        form = None
        view = inspect.currentframe().f_back.f_code.co_name
        method = eval("self." + FORMS[view])
        if method and callable(method):
            form = method(response=response, instance=instance)
        return form
