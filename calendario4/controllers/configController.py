from ..models import MyUser


class ConfigController:
    def __init__(self):
        self.user = MyUser()
        self.message = ""
