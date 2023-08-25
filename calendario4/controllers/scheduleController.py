from ..config.constants import WEEK_DAYS_LETTER
from ..controllers.utils import parse_colors
from ..logic.Schedule import Schedule
from ..models import Color
from .UserAdapter import UserAdapter


class ScheduleController:
    def __init__(self, year, user_id):
        self.year = year
        self.user = UserAdapter.get_user(self, user_id)
        self.my_user = UserAdapter.get_my_user(self, user_id)
        self.schedule = None

    def works(self):
        self.schedule = ScheduleController.find_user_schedule(self)
        if self.schedule:
            # TODO: DESPLEGAR EL SCHEDULE Y CREAR UNA
            # FUNCION PARA recuperarlo cuando se necesite
            self.deploy_schedule()
        else:
            data = self.prepare_data()
            self.schedule = self.create_schedule(data)
            self.copy_data_to_save()
        context = self.prepare_context()
        return context

    def prepare_data(self):
        team = self.my_user.team
        colors = parse_colors(Color.objects.get(user=self.user.id))

        data = [self.year, team, colors]
        return data

    def create_schedule(self, data):
        schedule = Schedule(*data)
        return schedule

    def prepare_context(self):
        return {"schedule": self.schedule, "weekdays": WEEK_DAYS_LETTER}
