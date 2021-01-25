import random

import click


@click.command()
@click.option(
    "--ban_list", type=str, help="List of champs to add to the ban pool", required=True
)
def run(ban_list):
    parsed_ban_list = ban_list.split(",")
    click.secho(f"Banning from: {str(parsed_ban_list)}")

    while True:
        if len(parsed_ban_list) == 1:
            click.secho(f"Banned champ: {parsed_ban_list[0]}", fg="red")
            break
        else:
            index_to_remove = random.randrange(0, len(parsed_ban_list))
            del parsed_ban_list[index_to_remove]


if __name__ == "__main__":
    run()
