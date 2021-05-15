# Generated by Django 3.2.3 on 2021-05-15 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Summoner",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("summoner_id", models.CharField(max_length=100, unique=True)),
                ("riot_account_id", models.CharField(max_length=100, unique=True)),
                ("player_uuid", models.CharField(max_length=100, unique=True)),
                ("in_game_name", models.CharField(max_length=255, unique=True)),
                (
                    "user_id",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]