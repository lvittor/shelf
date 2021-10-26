from pprint import pprint

import click
import inquirer
import yaml

branches=[
    "hotfix-",
    "release-",
    "develop-",
    "feature-",
]

branch_questions = [
    inquirer.Checkbox(
        "branches",
        message="Select the following branch categorization for your project.",
        choices=[
            "Feature",
            "Hotfix",
            "Bugfix",
            "Release",
            "Stage",
            "Test",
            "Experimental",
            "Build",
        ],
        default=["Feature"],
    )
]

trailer_questions = [
    inquirer.Checkbox(
        "trailers",
        message="Select the trailers you want to add to your project. Use the arrows to toggle any one of them.",
        choices=[
            "Acked-by",
            "Bug",
            "CC",
            "Change-Id",
            "Closes",
            "Closes-Bug",
            "Co-Authored-By",
            "DocImpact",
            "Git-Dch",
            "Implements",
            "Partial-Bug",
            "Related-Bug",
            "Reported-by",
            "SecurityImpact",
            "Signed-off-by",
            "Suggested-by",
            "Tested-by",
            "Thanks",
            "UpgradeImpact",
        ],
        default=["Acked-by"],
    ),
]

# TODO: erase after including descriptions in the choices list.
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
    config = {"trailers": [], "branches": []}

    ### Configuration for trailers
    selected_trailers = inquirer.prompt(trailer_questions)
    ### Configuration for branches
    selected_branches = inquirer.prompt(branch_questions)

    config["trailers"] = selected_trailers["trailers"]
    config["branches"] = selected_branches["branches"]

    with open(r"shelf-config.yaml", "w") as file:
        documents = yaml.dump(config, file)
    click.echo("Initialization successful")


@cli.command()
@click.option("--message", "-m", type=str, required=True)
def commit(message):
    a = message
    click.echo(f"{a}")

@cli.command()
@click.option("--new", "-n", type=str, required=False)
def branch(message):
    with open("shelf-config.yaml", "r") as file:
        documents = yaml.load(file)
    
    # para acceder: txt = documents["root"](<-- si es que hay)["branches"]
    a = message
    click.echo(f"{a}")


@cli.command()
def write():
    click.echo("Dropped the database")


if __name__ == "__main__":
    cli()
