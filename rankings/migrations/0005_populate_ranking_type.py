from django.db import migrations
from rankings.models import GAME_OPTIONS


def populate_ranking_type(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return

    model = apps.get_model("rankings", "RankingType")

    for ranking_type in GAME_OPTIONS:
        new_ranking_type = model.objects.create(value=ranking_type.value)
        new_ranking_type.save()


class Migration(migrations.Migration):
    dependencies = [
        ("rankings", "0004_auto_20210715_1933"),
    ]

    operations = [
        migrations.RunPython(populate_ranking_type, reverse_code=migrations.RunPython.noop)
    ]
