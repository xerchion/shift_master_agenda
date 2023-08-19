from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import AlterDay, Color, MyUser


class SignUpForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=200)
    password = forms.CharField(
        widget=forms.PasswordInput(), label="Contraseña", min_length=5,
        max_length=20
    )

    repeat_pass = forms.CharField(
        widget=forms.PasswordInput(),
        label="Repite la contraseña",
        min_length=5,
        max_length=20,
    )


class UserConfigForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ["name", "team", "category"]

    pswd_link = "Cambiar contraseña"


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update(
            {"class": "form-control"})
        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control"})
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control"})
        print(
            self.fields["new_password2"].widget.attrs.update(
                {"class": "form-control"})
        )

    # Prueba de campo con opciones, seleccionable


class BooleanSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        choices = ((True, "Si"), (False, "No"))
        super().__init__(*args, choices=choices, **kwargs)


class AlterDayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlterDayForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AlterDay
        fields = [
            "shift",
            "extra_hours",
            "keep_day",
            "change_payable",
            "comments",
        ]


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = (
            "morning",
            "afternoon",
            "night",
            "split_shift",
            "free",
            "holiday",
            "extra_holiday",
        )

        # Define los widgets para los campos de color
        widgets = {
            "morning": forms.TextInput(attrs={"type": "color"}),
            "afternoon": forms.TextInput(attrs={"type": "color"}),
            "night": forms.TextInput(attrs={"type": "color"}),
            "split_shift": forms.TextInput(attrs={"type": "color"}),
            "free": forms.TextInput(attrs={"type": "color"}),
            "own_business": forms.TextInput(attrs={"type": "color"}),
            "holiday": forms.TextInput(attrs={"type": "color"}),
            "extra_holiday": forms.TextInput(attrs={"type": "color"}),
        }
