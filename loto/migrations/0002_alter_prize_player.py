# Generated by Django 4.2.3 on 2023-09-07 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("loto", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prize",
            name="player",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="loto.player"
            ),
        ),
    ]
