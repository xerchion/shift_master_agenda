from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .config.constants import WEEK_DAYS_LETTER
from .controllers.alterDayController import AlterDayController
from .controllers.signUpController import SignUpController
from .controllers.UserAdapter import UserAdapter
from .forms import (ColorForm, CustomPasswordChangeForm, SignUpForm,
                    UserConfigForm)
from .models import Color, MyUser


def home(request):
    return render(request, "home.html")


def necessary_team(func):
    def wrapper(request, *args, **kwargs):
        user_adapter = UserAdapter()
        my_user = user_adapter.get_my_user(request.user.id)
        if my_user.team:
            return func(request, *args, **kwargs)
        else:
            return redirect("config")

    return wrapper


@login_required
def config(request):
    message = request.GET.get("data", "")

    user = MyUser.objects.get(user=request.user.id)
    if request.method == "POST":
        form = UserConfigForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("agenda")
    else:
        form = UserConfigForm(instance=user)
    context = {"form": form, "message": message}
    return render(request, "config.html", context)


def sign_up_view(request):
    controller = SignUpController(request)
    msg = ""
    if request.method == "POST":
        msg = controller.post()
        if controller.is_new_user:
            return redirect(f"/config/?data={controller.message}")
        else:
            form = SignUpForm(request.POST)
    else:
        form = SignUpForm()
    context = {"form": form, "msg": msg}
    return render(request, "registration/signup.html", context)


@login_required
def change_pass(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, "change_pass.html", {"form": form})


@login_required
def agenda(request):
    schedule = request.schedule
    weekdays = WEEK_DAYS_LETTER
    context = {"schedule": schedule, "weekdays": weekdays}
    return render(request, "agenda.html", context)


@login_required
def alter_day(request, date):
    schedule = request.schedule
    controller = AlterDayController(request.user.id, date, schedule)
    if request.method == "POST":
        controller.control_response(request)
        if controller.message != "exit":
            form = controller.form
        return redirect(controller.url_redirection)
    else:
        form = controller.without_post()
    context = {
        "day": controller.day,
        "month_name": controller.month_name,
        "form": form,
    }
    return render(request, "alter_day.html", context)


@login_required
def change_color_days(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    user_colors = Color.objects.get(user=user_id)

    if request.method == "POST":
        form = ColorForm(request.POST, instance=user_colors)
        if "restaurar_colores" in request.POST:
            user_adapter = UserAdapter()
            user_adapter.restart_colors(user)
            return redirect("change_color_days.html")

        if form.is_valid():
            colors = form.save(commit=False)
            colors.save()
            return redirect("agenda")
    else:
        saved = Color.objects.filter(user=user).first()
        if saved:
            form = ColorForm(instance=saved)
        else:
            form = ColorForm(instance=user)
    context = {"form": form}
    return render(request, "change_color_days.html", context)


@login_required
def recap_month(request, month):
    schedule = request.schedule
    month = int(month)
    month = schedule.months[month - 1]
    recap = month.calculate_recap()

    context = {"recap": recap}
    return render(request, "recap.html", context)


@login_required
def recap_year(request):
    schedule = request.schedule
    year = schedule.year
    recap = schedule.calculate_recap_year()

    context = {"year": year, "recap": recap}
    return render(request, "recap.html", context)
