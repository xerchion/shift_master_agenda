# calendario_middleware.py
from datetime import datetime

from django.urls import resolve

from ..config.constants import TEAMS_LIST
from ..controllers.AlterDayController import AlterDayController
from ..controllers.UserAdapter import UserAdapter
from ..logic.Schedule import Schedule


class ScheduleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            views_with_schedule = ["agenda", "alter_day", "recap_month", "recap_year"]
            current_view = resolve(request.path_info).url_name
            if current_view in views_with_schedule:
                user = UserAdapter(request.user.id)
                team = user.get_team()
                schedule = None
                if team in TEAMS_LIST:
                    colors = user.get_colors()
                    schedule = Schedule(datetime.today().year, team, colors)
                    schedule = AlterDayController.load_alter_days_db(
                        request.user, schedule
                    )
                    schedule.fill_colors()

                request.schedule = schedule
            else:
                ...
        else:
            ...
        response = self.get_response(request)
        return response
