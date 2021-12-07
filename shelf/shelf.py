import os
import re
from pprint import pprint

import click
import inquirer
import yaml

branch_questions = [
    inquirer.Checkbox(
        "branches",
        message="Select the following branch categorization for your project",
        choices=[
            "Release",
            "Develop",
            "Feature",
            "Hotfix",
            "Bugfix",
            "Stage",
            "Test",
            "Experimental",
            "Build",
        ],
        default=["Release", "Develop", "Feature", "Hotfix"],
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


def get_branch_rules(branch_name, branches):
    branch = {}
    click.echo(f'Configuration of rules for branch "{branch_name}".')
    branch["name"] = branch_name.lower()
    branch["parent"] = inquirer.list_input(
        "Will checkout from and merge into",
        choices=[branch for branch in branches if branch != branch_name] + ["Main"],
    )
    branch["unique"] = inquirer.confirm(f"Is the branch {branch_name} unique?")
    if not branch["unique"]:
        branch["regex"] = inquirer.text(
            message="Enter the regex which will identify the branch"
        )

    return branch


def create_branches(branches_keys, branches_dict):
    ## TODO: Topological sort
    for branch in branches_keys:
        print(
            os.system(
                f'git show-ref --verify --quiet refs/heads/{branches_dict[branch]["name"]}'
            )
        )
        if os.system(
            f'git show-ref --verify --quiet refs/heads/{branches_dict[branch]["name"]}'
        ):
            click.echo(
                f'git checkout {branches_dict[branches_dict[branch]["parent"]]["name"]}'
            )
            os.system(
                f'git checkout {branches_dict[branches_dict[branch]["parent"]]["name"]}'
            )
            click.echo(f'git branch {branches_dict[branch]["name"]}')
            os.system(f'git branch {branches_dict[branch]["name"]}')


@click.group()
def cli():
    pass


@cli.command()
def init():
    click.echo("Initializing shelf repository")

    ### Configuration of git repository
    if os.system("git init") or os.system(
        'git commit --allow-empty -m "Shelf initialization"'
    ):
        raise click.Abort()

    config = {"trailers": [], "branches": {}}
    ### Configuration for trailers
    selected_trailers = inquirer.prompt(trailer_questions)
    config["trailers"] = selected_trailers["trailers"]

    ### Configuration for branches
    selected_branches = inquirer.prompt(branch_questions)
    branches = {}
    for branch in selected_branches["branches"]:
        branches[branch] = get_branch_rules(branch, selected_branches["branches"])
    branches["Main"] = {"name": "master", "unique": True, "parent": None}
    click.echo("git rev-parse --abbrev-ref HEAD")
    os.system("git rev-parse --abbrev-ref HEAD")
    config["branches"] = branches

    with open(r"shelf-config.yaml", "w") as file:
        documents = yaml.dump(config, file)

    unique_branches = [
        branch for branch in config["branches"] if config["branches"][branch]["unique"]
    ]
    create_branches(unique_branches, config["branches"])

    click.echo("Initialization successful")


@cli.command()
@click.option("--message", "-m", type=str, required=True)
def commit(message):
    a = message
    click.echo(f"Mensaje inicial: {a}")


@cli.command()
@click.option("--name", "-n", type=str, required=True)
def branch(name):
    with open("shelf-config.yaml", "r") as file:
        documents = yaml.safe_load(file)
    target_branch = None

    for branch in documents["branches"]:
        if (not documents["branches"][branch]["unique"]) and re.fullmatch(
            documents["branches"][branch]["regex"], name
        ):
            print(branch)
            print(documents["branches"][branch]["regex"])
            print(re.fullmatch(documents["branches"][branch]["regex"], name))
            target_branch = branch
    if target_branch is None:
        click.echo("Not a valid branch format.")
        click.echo("The new branch name should follow one of the following patterns:")
        for i in documents["branches"]:
            if not documents["branches"][i]["unique"]:
                click.echo(f'{documents["branches"][i]["regex"]} for a {i} branch')
    else:
        click.echo(
            f'os: git checkout {documents["branches"][documents["branches"][target_branch]["parent"]]["name"]}'
        )
        click.echo(f"os: git checkout -b {name}")
        click.echo(f"Branch {name} created succesfully")
    # Call to git function

    # para acceder: txt = documents["root"](<-- si es que hay)["branches"]


if __name__ == "__main__":
    cli()
