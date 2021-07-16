from django.db import migrations
from roles.models import VALORANT_ROLE


def populate_valorant_roles_enum(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return

    model = apps.get_model("roles", "ValorantRole")

    for role in VALORANT_ROLE:
        new_role = model.objects.create(value=role.value)
        new_role.save()


class Migration(migrations.Migration):
    dependencies = [
        ("roles", "0004_auto_20210715_2004"),
    ]

    operations = [migrations.RunPython(populate_valorant_roles_enum, reverse_code=migrations.RunPython.noop)]
