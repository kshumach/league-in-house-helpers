import click

from utils.perma_banner import ban_from


@click.command()
@click.option(
    "--ban_list", type=str, help="List of champs to add to the ban pool", required=True
)
def run(ban_list):
    parsed_ban_list = ban_list.split(",")
    click.secho(f"Banning from: {str(parsed_ban_list)}")

    banned = ban_from(parsed_ban_list)

    click.secho(f"Banned champ: {banned}", fg="red")


if __name__ == "__main__":
    run()
