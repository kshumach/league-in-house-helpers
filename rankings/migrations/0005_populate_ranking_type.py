from django.db import migrations
from rankings.models import RANKING_TYPE


def populate_ranking_type(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return

    model = apps.get_model("rankings", "RankingType")

    for ranking_type in RANKING_TYPE:
        new_ranking = model.objects.create(value=ranking_type.value)
        new_ranking.save()


class Migration(migrations.Migration):
    dependencies = [
        ("rankings", "0004_auto_20210715_1933"),
    ]

    operations = [
        migrations.RunPython(populate_ranking_type, reverse_code=migrations.RunPython.noop)
    ]
