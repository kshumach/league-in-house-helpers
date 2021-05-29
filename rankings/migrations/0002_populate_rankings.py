from django.db import migrations
from rankings.models import RANKING


def populate_rankings_enum(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return

    model = apps.get_model("rankings", "Ranking")

    for ranking in RANKING:
        new_ranking = model.objects.create(value=ranking.value)
        new_ranking.save()


class Migration(migrations.Migration):
    dependencies = [
        ("rankings", "0001_initial"),
    ]

    operations = [migrations.RunPython(populate_rankings_enum, reverse_code=migrations.RunPython.noop)]
