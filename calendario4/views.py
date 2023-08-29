from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .config.constants import WEEK_DAYS_LETTER
from .controllers.AlterDayController import AlterDayController
from .controllers.SignUpController import SignUpController
from .controllers.UserAdapter import UserAdapter
from .forms import (ColorForm, CustomPasswordChangeForm, SignUpForm,
                    UserConfigForm)
from .models import Color


def home(request):
    return render(request, "home.html")


def necessary_team(func):
    def wrapper(request, *args, **kwargs):
        # TODO INTENTA ELIMINAR ESTO, USA DIRECTAMENTE EL ADAPTADOR SIN USAR VARIABLE INTERMEDIA
        # PARACE QUE SOLO SE USA AQUI LA DE GET_MY_USER ASI QUE PUEDES PROBAR A CONVERTIRLA
        # EN UN METODO DE CLASE DIRECTAMENTE....
        user_adapter = UserAdapter(request.user.id)
        my_user = user_adapter.get_my_user()
        print(my_user.team, "----------------------------------")
        team = UserAdapter(request.user.id).team
        print(team, my_user.team)
        if my_user.team:
            return func(request, *args, **kwargs)
        else:
            return redirect("config")

    return wrapper


@login_required
def config(request):
    message = request.GET.get("data", "")
    user = request.user
    my_user = UserAdapter(user.id).get_my_user()
    if request.method == "POST":
        form = UserConfigForm(request.POST, instance=my_user)
        if form.is_valid():
            form.save()
            return redirect("agenda")
    else:
        form = UserConfigForm(instance=my_user)
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
# @necessary_team
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
        form = controller.generate_form()
    context = {"day": controller.day, "month_name": controller.month_name, "form": form}
    return render(request, "alter_day.html", context)


@login_required
def change_color_days(request):
    user_id = request.user.id
    user = request.user
    user_colors = Color.objects.get(user=user_id)

    if request.method == "POST":
        form = ColorForm(request.POST, instance=user_colors)
        if "restaurar_colores" in request.POST:
            UserAdapter(user.id).apply_default_colors()
            return redirect("config")

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
    month.calculate_recap()
    recap = month.recap

    context = {"recap": recap}
    return render(request, "recap.html", context)


@login_required
def recap_year(request):
    schedule = request.schedule
    year = schedule.year
    recap = schedule.calculate_recap_year()
    context = {"year": year, "recap": recap}
    return render(request, "recap.html", context)
