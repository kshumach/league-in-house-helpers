from django.db import migrations
from rankings.models import RANKING_TYPE, RankingType


def add_default_user_ranking_type(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return

    model = apps.get_model("rankings", "UserRanking")

    default_ranking = RankingType.objects.get(value=RANKING_TYPE.LEAGUE.value)

    model.objects.all().update(ranking_type=default_ranking)


class Migration(migrations.Migration):
    dependencies = [
        ("rankings", "0005_populate_ranking_type"),
    ]

    operations = [
        migrations.RunPython(add_default_user_ranking_type, reverse_code=migrations.RunPython.noop)
    ]
