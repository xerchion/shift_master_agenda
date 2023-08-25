from django.urls import include, path

from .views import (agenda, alter_day, change_color_days, change_pass, config,
                    home, recap_month, recap_year, sign_up_view)

urlpatterns = [
    path("", home, name="home"),
    path("agenda/", agenda, name="agenda"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", sign_up_view, name="signup"),
    path("config/", config, name="config"),
    path("change_pass/", change_pass, name="change_pass"),
    path("change_color_days/", change_color_days, name="change_color_days"),
    path("alter_day/<str:date>/", alter_day, name="alter_day"),
    path("recap_month/<str:month>/", recap_month, name="recap_month"),
    path("recap_year/", recap_year, name="recap_year"),
]
