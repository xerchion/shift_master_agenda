from django.contrib.auth import login, logout

from ..config.constants import (NAME_USER_EXISTS, PASSWORDS_NOT_MATCH,
                                USER_SIGNUP_OK)
from ..forms import SignUpForm
from ..models import MyUser
from .UserAdapter import UserAdapter


class SignUpController:
    def __init__(self, request):
        self.user = MyUser()
        self.response = request.POST
        self.request = request
        self.form = None
        self.user_adapter = UserAdapter()
        self.user_name = self.response.get("username")
        self.password = self.response.get("password")
        self.repeat_pass = self.response.get("repeat_pass")
        self.is_new_user = False
        self.message = ""

    def singup_user(self, user):
        if self.user_adapter.exists(user.user_name):
            self.message = NAME_USER_EXISTS
            new_user = False
        else:
            self.message = USER_SIGNUP_OK
            new = self.user_adapter.add_new_user(user.user_name, user.password, None)
            new_user = new.user
        return (new_user, self.message)

    def post(self):
        self.form = SignUpForm(self.response)
        if self.form.is_valid():
            if self.pass_equals():
                user = self.user_adapter.create_new_my_user(
                    self.user_name, self.password
                )
                logout(self.request)
                new_user, self.message = self.singup_user(user)
                if new_user:
                    login(self.request, new_user)
                    self.is_new_user = True
            else:
                self.message = PASSWORDS_NOT_MATCH
        return self.message

    def pass_equals(self):
        return self.password == self.repeat_pass
