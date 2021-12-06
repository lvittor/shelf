import click
import yaml


@click.group()
def cli():
    pass


@cli.command()
def init():
    click.echo("Initializing shelf repository")
    ### Creation of the config file
    config = {}

    ### Configuration for trailers
    click.echo("Select the default trailers for your repository: ")
    config["trailers"] = []
    for trailer in trailers:
        while True:
            response = input(trailer["name"] + "(Y/N): ").upper()
            if response in ["Y", "N"]:
                break
        if response == "Y":
            config["trailers"].append(trailer["name"])
            click.echo("Trailer added to config file")
        else:
            click.echo("Trailer excluded from config file")

    with open(r"shelf-config.yaml", "w") as file:
        documents = yaml.dump(config, file)
    click.echo("Initialization successful")


@cli.command()
@click.option("--message", "-m", type=str, required=True)
def commit(message):
    a = message
    click.echo(f"{a}")


@cli.command()
def write():
    click.echo("Dropped the database")


if __name__ == "__main__":
    cli()
