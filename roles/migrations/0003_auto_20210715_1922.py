# Generated by Django 3.2.3 on 2021-07-15 23:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roles', '0002_populate_roles'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Role',
            new_name='LeagueRole',
        ),
        migrations.RenameModel(
            old_name='UserRolePreference',
            new_name='UserLeagueRolePreference',
        ),
    ]
