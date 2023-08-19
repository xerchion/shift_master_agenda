from django.urls import include, path

from .views import (agenda, alter_day, change_password, config, home,
                    recap_month, recap_year, sign_up_view, user_color_change)

urlpatterns = [
    path("", home, name="home"),
    path("agenda/", agenda, name="agenda"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", sign_up_view, name="signup"),
    path("config/", config, name="config"),
    path("changePassword/", change_password, name="changePassword"),
    path("userColorChange/", user_color_change, name="userColorChange"),
    path("alterDay/<str:date>/", alter_day, name="alterDay"),
    path("recapMonth/<str:month>/", recap_month, name="recapMonth"),
    path("recapYear/", recap_year, name="recapYear"),
]
