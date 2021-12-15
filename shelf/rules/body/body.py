from ..rule import Rule


class BodyRule(Rule):
    body = []

    def __init__(self, body: list):
        super().__init__()
        self.body = body


class MaxLengthBodyRule(BodyRule):
    MAX_LEN = 80

    def check(self) -> bool:
        for line in self.body:
            if len(line) > self.MAX_LEN:
                return False
        return True

    def __str__(self):
        return (
            f"Body of commit message should be shorter than {self.MAX_LEN} characters"
        )


class MinLengthBodyRule(BodyRule):
    MIN_LEN = 20

    def check(self) -> bool:
        for line in self.body:
            if len(line) < self.MIN_LEN and line != "":
                return False
        return True

    def __str__(self):
        return f"Body of commit message should be larger than {self.MIN_LEN} characters"


class TrailingWhitespaceBodyRule(BodyRule):
    def check(self) -> bool:
        for line in self.body:
            if line.endswith(" "):
                return False
        return True

    def __str__(self):
        return f"Body of commit message should not have trailing whitespaces"


class HardTabBodyRule(BodyRule):
    def check(self) -> bool:
        for line in self.body:
            if "\t" in line:
                return False
        return True

    def __str__(self):
        return f"Body of commit message should not contain hard tab characters (\\t)"


class BodyMissingBodyRule(BodyRule):
    def check(self) -> bool:
        return False if not self.body else True

    def __str__(self):
        return f"Body message must be specified"
