import click
from error_handler import ErrorHandler


class Context:
    def __init__(self, msg_filename):
        self.msg_filename = msg_filename


@click.group()
@click.option(
    "--msg-filename",
    help="Path to a file containing a commit message.",
)
@click.pass_context
def cli(ctx, msg_filename):
    ctx.obj = Context(msg_filename)


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
    for error in errors:
        print(error)
    ctx.exit(len(errors))


if __name__ == "__main__":
    cli()
