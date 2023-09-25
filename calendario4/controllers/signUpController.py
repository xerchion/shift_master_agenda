#  Only for type annotations
from typing import Tuple

from django.contrib.auth import login, logout
from django.http import HttpRequest  # Only for type annotations

from ..config.constants import (FORM_NOT_VALID, NAME_USER_EXISTS,
                                NECESSARY_TEAM, PASSWORDS_NOT_MATCH,
                                USER_SIGNUP_OK)
from ..forms import SignUpForm
# Only for type annotations
from ..models import User
from .UserAdapter import UserAdapter


class SignUpController:
    def __init__(self, request: HttpRequest):
        self.user = None
        self.response = request.POST
        self.request = request
        self.form = SignUpForm()
        self.user_adapter = UserAdapter()
        self.user_name = self.response.get("username")
        self.password = self.response.get("password")
        self.repeat_pass = self.response.get("repeat_pass")
        self.is_new_user = False
        self.message = ""

    def signup_user(self, user: User) -> Tuple[bool, str]:
        """
        Registers a new user.

        Args:
            user (User): The user data to be registered.

        Returns:
            False if the user already exists, or the user if it was successfully created.
        """
        new = False
        if self.user_adapter.exists(user.user_name):
            self.message = NAME_USER_EXISTS
        else:
            self.message = USER_SIGNUP_OK
            new = self.user_adapter.add_new_user(
                user.user_name, user.password, None
            ).user
        return (new, self.message)

    def handle_signup_post(self) -> None:
        """
        Handles the POST request for user signup.

        """
        self.form = SignUpForm(self.response)
        if self.form.is_valid():
            if self.pass_equals():
                user = self.user_adapter.create_new_my_user(
                    self.user_name, self.password
                )
                logout(self.request)
                new_user, self.message = self.signup_user(user)
                if new_user:
                    login(self.request, new_user)
                    self.message = NECESSARY_TEAM
                    self.is_new_user = True
            else:
                self.message = PASSWORDS_NOT_MATCH
        else:
            self.message = FORM_NOT_VALID

    def pass_equals(self) -> bool:
        return self.password == self.repeat_pass
