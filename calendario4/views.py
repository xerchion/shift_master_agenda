from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .config.constants import WEEK_DAYS_LETTER
from .controllers.AlterDayController import AlterDayController
from .controllers.SignUpController import SignUpController
from .controllers.UserAdapter import UserAdapter
from .logic.Recap import Recap


def home(request):
    return render(request, "home.html")


@login_required
def config(request):
    message = request.GET.get("data", "")
    id = request.user.id
    if request.method == "POST":
        form = UserAdapter(id).get_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("agenda")
    else:
        form = UserAdapter(id).get_form()
    context = {"form": form, "message": message}
    return render(request, "config.html", context)


def sign_up_view(request):
    controller = SignUpController(request)
    if request.method == "POST":
        controller.handle_signup_post()
        if controller.is_new_user:
            # return redirect(f"/config/?data={controller.message}")
            from django.http import HttpResponseRedirect
            from django.urls import reverse

            return HttpResponseRedirect(
                reverse("config") + f"?msg={controller.message}"
            )

    form = controller.form
    context = {"form": form, "msg": controller.message}
    return render(request, "registration/signup.html", context)


@login_required
def change_pass(request):
    id = request.user.id
    if request.method == "POST":
        form = UserAdapter(id).get_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserAdapter(id).get_form()

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
    controller = AlterDayController(
        request.user.id,
        date,
        schedule,
    )
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
    user = UserAdapter(request.user.id)

    if request.method == "POST":
        # form = user.set_color_form(request.POST, instance=user.colors)
        form = UserAdapter(request.user.id).set_color_form(
            request.POST, instance=user.colors
        )

        if "restaurar_colores" in request.POST:
            user.apply_default_colors()
            return redirect("config")
        if form.is_valid():
            user.colors = form.save(commit=False)
            user.colors.save()
            return redirect("agenda")
    else:
        if user.color_saved:
            form = user.get_form(instance=user.color_saved)
        else:
            form = user.get_form()

    context = {"form": form}
    return render(request, "change_color_days.html", context)


@login_required
def recap_month(request, month):
    month = request.schedule.months[int(month) - 1]

    recap = Recap.calculate(month, month.name)
    context = {"recap": recap}
    return render(request, "recap.html", context)


@login_required
def recap_year(request):
    recap = Recap.calculate(request.schedule.months, request.schedule.year)
    context = {"year": request.schedule.year, "recap": recap}
    return render(request, "recap.html", context)
