import inspect
from typing import Optional, Union  # Only for type annotations

from django.contrib.auth.models import User
from django.http import HttpRequest  # Only for type annotations

from ..config.constants import (BASE_DAY_COLORS, EVENING, EXTRA_HOLIDAY, FORMS,
                                FREE_DAY, HOLIDAY, MORNING, NIGHT, SPLIT)
from ..controllers.utils import create_color_mapping
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

    def add_new_user(self, name: str, pswd: str, team: str) -> "UserAdapter":
        """
        Returns:
            UserAdapter: An instance of UserAdapter for the newly created user.
        """
        new_user = User.objects.create_user(username=name, password=pswd)
        new_user.save()
        self.user = new_user

        new_my_user = MyUser(user_name=name, user=new_user, team=team)
        new_my_user.save()
        self.my_user = new_my_user

        self.apply_default_colors()

        return UserAdapter(new_user.id)

    def create_new_my_user(self, name: str, password: str) -> MyUser:
        return MyUser(user_name=name, password=password)

    @classmethod
    def get_user(cls, id: int) -> User:
        return User.objects.get(id=id)

    def apply_default_colors(self) -> None:
        """
        Applies default colors to the user.

        """
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

    def exists(self, data: Union[int, str]) -> bool:
        """
        Checks if a user with the given data exists.

        Args:
            data (Union[int, str]): The data to check. Can be either an ID (int) or a username (str).

        Returns:
            bool: True if a user with the given data exists, False otherwise.
        """
        if isinstance(data, int):
            return User.objects.filter(id=data).exists()
        elif isinstance(data, str):
            return User.objects.filter(username=data).exists()

    def get_colors(self) -> dict:
        """
        Gets the color mapping associated with the user.

        Returns:
            dict: A dictionary containing the user's color preferences.
        """
        return create_color_mapping(Color.objects.get(user=self.id))

    # TODO NO USADO
    def set_team(self, team: str) -> None:
        """
        Sets the team for the user.

        Args:
            team (TeamType): The team to assign to the user.

        """
        self.my_user.team = team

    def get_team(self) -> str:
        """
        Returns the team associated with the user.

        """
        return self.my_user.team

    @classmethod
    @property
    def team(cls) -> Union[None, MyUser]:
        """
        Gets the team associated with the user class.

        Returns:
        Union[MyUser, None]: The team of the user class if found, else None.
        """
        try:
            return MyUser.objects.get(user=cls.id).team
        except MyUser.DoesNotExist:
            return None

    def set_color_form(self, response: HttpRequest, instance: Color) -> ColorForm:
        """
        Sets the color form with the provided response and instance.

        Args:
            response (HttpRequest): The HTTP request object.
            instance (Color): The Color instance.

        Returns:
            ColorForm: The ColorForm instance.
        """
        # TODO PORQUE LO ASIGNA AL ATRIBUTO DE INSTANCIA Y TAMBIEN LO DEVUELVE???????
        self.color_form = ColorForm(response, instance=instance)
        return self.color_form

    @property
    def color_saved(self) -> Union[Color, None]:
        """
        Gets the saved color associated with the user.

        Returns:
           The Color object if found, else None.
        """
        return Color.objects.filter(user=self.user).first()

    def get_color_form(self, instance=None, response=None):
        return (
            ColorForm(instance=instance) if instance else ColorForm(instance=self.user)
        )

    def get_config_form(
        self,
        response: Union[HttpRequest, None] = None,
        instance: Union[MyUser, None] = None,
    ) -> UserConfigForm:
        """
        Gets the user configuration form.

        Args:
            response (HttpRequest, optional): The HTTP request object. Defaults to None.
            instance (MyUser, optional): The MyUser instance. Defaults to None.

        Returns:
            UserConfigForm: The UserConfigForm instance.
        """
        if response:
            form = UserConfigForm(response, instance=self.my_user)
        else:
            form = UserConfigForm(instance=self.my_user)
        return form

    def get_pass_form(
        self, response: Optional[HttpRequest] = None, instance: Optional[MyUser] = None
    ) -> CustomPasswordChangeForm:
        """
        Gets the password change form.

        Args:
            response (HttpRequest, optional): The HTTP request object. Defaults to None.
            instance (MyUser, optional): The MyUser instance. Defaults to None.

        Returns:
            CustomPasswordChangeForm: The CustomPasswordChangeForm instance.
        """
        if response:
            form = CustomPasswordChangeForm(self.user, response)
        else:
            form = CustomPasswordChangeForm(self.user)
        return form
    from django.forms import Form

    def get_form(
        self, response: Optional[HttpRequest] = None, instance: Optional[MyUser] = None
    ) -> Optional[Form]:
        """
        Gets the form based on the current view.

        Args:
            response (HttpRequest, optional): The HTTP request object. Defaults to None.
            instance (MyUser, optional): The MyUser instance. Defaults to None.

        Returns:
            Optional[Form]: The form instance or None if no valid method is found.
        """
        form = None
        view = inspect.currentframe().f_back.f_code.co_name
        method = eval("self." + FORMS.get(view))

        if method and callable(method):
            form = method(response=response, instance=instance)

        return form
