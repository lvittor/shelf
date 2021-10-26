from ..rule import Rule


class Body(Rule):
    def __init__(self, commit_msg: str):
        super().__init__(commit_msg)
        self.header = commit_msg.split("\n")[1:]
