import os
import re
import subprocess
from pprint import pprint

import click
import inquirer
import yaml
from error_handler import ErrorHandler
from utils import get_current_branch

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

keywords_questions = [
    inquirer.Checkbox(
        "header_keywords",
        message="Select the valid keywords for commit headers",
        choices=[
            "Add",
            "Drop",
            "Fix",
            "Bump",
            "Make",
            "Start",
            "Stop",
            "Optimize",
            "Document",
            "Refactor",
            "Reformat",
            "Rearrange",
            "Redraw",
            "Reword",
        ],
        default=["Add", "Fix", "Refactor", "Reformat"],
    )
]


trailer_questions = [
    inquirer.Checkbox(
        "trailers",
        message="Select the trailers you want to add to your project. Use the arrows to toggle any one of them",
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


class DefaultCommandGroup(click.Group):
    """allow a default command for a group"""

    def command(self, *args, **kwargs):
        default_command = kwargs.pop("default_command", False)
        if default_command and not args:
            kwargs["name"] = kwargs.get("name", "<>")
        decorator = super(DefaultCommandGroup, self).command(*args, **kwargs)

        if default_command:

            def new_decorator(f):
                cmd = decorator(f)
                self.default_command = cmd.name
                return cmd

            return new_decorator

        return decorator

    def resolve_command(self, ctx, args):
        try:
            # test if the command parses
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)
        except click.UsageError:
            # command did not parse, assume it is the default command
            args.insert(0, self.default_command)
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)


@click.group(cls=DefaultCommandGroup)
@click.option(
    "--msg-filename",
    help="Path to a file containing a commit message.",
)
@click.pass_context
def cli(ctx, msg_filename):
    ctx.obj = Context(msg_filename)


@cli.command(
    default_command=True,
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.argument("args", nargs=-1)
def git(args):
    subprocess.call(["git"] + list(args))


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
            message=f"Enter the regex which will identify {branch_name}"
        )

    return branch


def create_branches(branches_keys, branches_dict):
    for branch in branches_keys:
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


@cli.command()
def init():

    click.echo("")
    click.echo("  ███████╗██╗  ██╗███████╗██╗     ███████╗    ")
    click.echo("  ██╔════╝██║  ██║██╔════╝██║     ██╔════╝    ")
    click.echo("  ███████╗███████║█████╗  ██║     █████╗      ")
    click.echo("  ╚════██║██╔══██║██╔══╝  ██║     ██╔══╝      ")
    click.echo("  ███████║██║  ██║███████╗██████████╗    ██║  ")
    click.echo("  ╚══════╝╚═╝  ╚═╝╚══════╝╚═════════╝    ╚═╝  ")
    click.echo("")

    click.echo("Initializing shelf repository")

    ### Configuration of git repository
    if os.system("git init") or os.system(
        'git commit --allow-empty -m "Add shelf init"'
    ):
        raise click.Abort()

    with open(".git/hooks/commit-msg", "w") as commit_msg:
        commit_msg.write(
            '#!/bin/sh\nshelf --msg-filename "$1" run-hook\nexit_code=$?\nexit $exit_code\n'
        )

    os.chmod(".git/hooks/commit-msg", 0o777)

    config = {"header_keywords": {}, "trailers": [], "branches": {}}
    ### Configuration for header_keywords
    selected_header_keywords = inquirer.prompt(keywords_questions)
    config["header_keywords"] = selected_header_keywords["header_keywords"]

    ### Configuration for trailers
    selected_trailers = inquirer.prompt(trailer_questions)
    config["trailers"] = selected_trailers["trailers"]

    ### Configuration for branches
    selected_branches = inquirer.prompt(branch_questions)
    branches = {}
    for branch in selected_branches["branches"]:
        branches[branch] = get_branch_rules(branch, selected_branches["branches"])
    branches["Main"] = {"unique": True, "parent": None, "name": get_current_branch()}
    config["branches"] = branches

    with open(r"shelf.yml", "w") as file:
        documents = yaml.dump(config, file)

    unique_branches = [
        branch for branch in config["branches"] if config["branches"][branch]["unique"]
    ]
    create_branches(unique_branches, config["branches"])

    click.echo("Initialization successful")


class Context:
    def __init__(self, msg_filename):
        self.msg_filename = msg_filename


@cli.command("run-hook")
@click.pass_context
def run_hook(ctx):
    msg_filename = ctx.obj.msg_filename

    try:
        file = open(msg_filename, "r")
        message = file.read()
    finally:
        file.close()
    errors = ErrorHandler.check_commit_msg(commit_msg=message)
    print("-----------------------------")
    print(message)
    print("-----------------------------")
    for error in errors:
        print(error)
    ctx.exit(len(errors))


@cli.command()
@click.option("--name", "-n", "name", type=str, required=True)
def start(name):
    with open("shelf.yaml", "r") as file:
        documents = yaml.safe_load(file)
    target_branch = None

    for branch in documents["branches"]:
        if (not documents["branches"][branch]["unique"]) and re.fullmatch(
            documents["branches"][branch]["regex"], name
        ):
            target_branch = branch
            break
    if target_branch is None:
        click.echo("Not a valid branch format.")
        click.echo("The new branch name should follow one of the following patterns:")
        for i in documents["branches"]:
            if not documents["branches"][i]["unique"]:
                click.echo(f'{documents["branches"][i]["regex"]} for a {i} branch')
        raise click.Abort()
    click.echo(
        f'git checkout {documents["branches"][documents["branches"][target_branch]["parent"]]["name"]}'
    )
    os.system(
        f'git checkout {documents["branches"][documents["branches"][target_branch]["parent"]]["name"]}'
    )
    click.echo(f"git checkout -b {name}")
    os.system(f"git checkout -b {name}")
    click.echo(f"Branch {name} created succesfully")
    # Call to git function

    # para acceder: txt = documents["root"](<-- si es que hay)["branches"]


@cli.command()
@click.option("--delete", "-d", is_flag=True)
def finish(delete):
    with open("shelf.yml", "r") as file:
        documents = yaml.safe_load(file)
    curr_branch = get_current_branch()
    for branch, rules in documents["branches"].items():
        if rules["unique"]:
            if rules["name"] == curr_branch:
                subprocess.call(
                    ["git", "checkout", documents["branches"][rules["parent"]]["name"]]
                )
                subprocess.call(["git", "merge", curr_branch])
        else:
            if re.fullmatch(rules["regex"], curr_branch):
                subprocess.call(
                    ["git", "checkout", documents["branches"][rules["parent"]]["name"]]
                )
                subprocess.call(["git", "merge", curr_branch])
                if delete:
                    subprocess.call(["git", "branch", "-d", curr_branch])


if __name__ == "__main__":
    cli()
