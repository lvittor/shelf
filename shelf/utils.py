import subprocess


def get_git_directory() -> str:
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode(
        "UTF-8"
    )[:-1]


def is_branch_created(branch: str) -> str:
    return not subprocess.call(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"]
    )


def get_current_branch() -> str:
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode(
        "UTF-8"
    )[:-1]
