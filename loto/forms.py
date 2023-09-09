from django import forms

from .models import Prize


class PrizeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrizeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Prize
        fields = [
            "date",
            "prize",
            "player",
        ]


class SimplePrizeForm(forms.Form):
    prize = forms.CharField(label="Premio de esta semana", max_length=200)
