from django.db import migrations
from roles.models import LEAGUE_ROLE


def populate_roles_enum(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return

    model = apps.get_model("roles", "Role")

    for role in LEAGUE_ROLE:
        new_role = model.objects.create(value=role.value)
        new_role.save()


class Migration(migrations.Migration):
    dependencies = [
        ("roles", "0001_initial"),
    ]

    operations = [migrations.RunPython(populate_roles_enum, reverse_code=migrations.RunPython.noop)]
