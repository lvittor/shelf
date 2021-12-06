from ..rule import Rule


class BodyRule(Rule):
    body = ""

    def __init__(self, body: str):
        super().__init__()
        self.body = body


class MaxLengthBodyRule(BodyRule):
    MAX_LEN = 80

    def check(self) -> bool:
        return len(self.body) <= self.MAX_LEN

    def __str__(self):
        return (
            f"Body of commit message should be shorter than {self.MAX_LEN} characters"
        )


class MinLengthBodyRule(BodyRule):
    MIN_LEN = 20

    def check(self) -> bool:
        return len(self.body) >= self.MAX_LEN

    def __str__(self):
        return f"Body of commit message should be larger than {self.MIN_LEN} characters"


class TrailingWhitespaceBodyRule(BodyRule):
    def check(self) -> bool:
        return self.body.endswith(" ")

    def __str__(self):
        return f"Body of commit message should not have trailing whitespaces"


class HardTabBodyRule(BodyRule):
    def check(self) -> bool:
        return "\t" in self.body

    def __str__(self):
        return f"Body of commit message should not contain hard tab characters (\\t)"


class BodyMissingBodyRule(BodyRule):
    def check(self) -> bool:
        return not self.body

    def __str__(self):
        return f"Body message must be specified"
