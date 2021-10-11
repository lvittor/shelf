import click
import yaml

trailers = [
    {
        "name": "Acked-by",
        "description": 'Owner of the affected code said "yep, looks good to me" ',
    },
    {
        "name": "Bug",
        "description": "References a bug in the Mediawiki Bugzilla installation ",
    },
    {"name": "CC", "description": "Person has been informed about the patch "},
    {
        "name": "Change-Id",
        "description": "unique identification of a change that persists rebasing and amending ",
    },
    {"name": "Closes", "description": "Closes a bug"},
    {"name": "Closes-Bug", "description": ""},
    {"name": "Co-Authored-By", "description": ""},
    {"name": "DocImpact", "description": ""},
    {"name": "Git-Dch", "description": ""},
    {"name": "Implements", "description": ""},
    {"name": "Partial-Bug", "description": ""},
    {"name": "Related-Bug", "description": ""},
    {"name": "Reported-by", "description": ""},
    {"name": "Reviewed-by", "description": ""},
    {"name": "SecurityImpact", "description": ""},
    {"name": "Signed-off-by", "description": ""},
    {"name": "Suggested-by", "description": ""},
    {"name": "Tested-by", "description": ""},
    {"name": "Thanks", "description": ""},
    {"name": "UpgradeImpact", "description": ""},
]


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
            response = input(trailer["name"] + " (Y/N) ").upper()
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
def commit():
    click.echo("Before commiting, specify the following trailers: ")


@cli.command()
def write():
    click.echo("Dropped the database")


if __name__ == "__main__":
    cli()
