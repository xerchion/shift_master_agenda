# calendario_middleware.py
from datetime import datetime

from django.contrib.auth.models import User
from django.urls import resolve

from ..config.constants import TEAMS_LIST
from ..controllers.utils import parse_colors
from ..logic.Schedule import Schedule
from ..models import Color, MyUser


class ScheduleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            views_with_schedule = ["agenda", "alterDay", "recapMonth",
                                   "recapYear"]
            current_view = resolve(request.path_info).url_name
            if current_view in views_with_schedule:
                user_id = request.user.id
                my_user = MyUser.objects.get(user=user_id)
                user = User.objects.get(id=user_id)

                colors = parse_colors(Color.objects.get(user=user_id))
                schedule = None

                if my_user.team in TEAMS_LIST:
                    schedule = Schedule(datetime.today().year, my_user.team,
                                        colors)
                    schedule.load_alter_days_db(user)

                request.schedule = schedule

        response = self.get_response(request)
        return response
