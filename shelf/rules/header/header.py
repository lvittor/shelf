from ..rule import Rule


class HeaderRule(Rule):
    header = ""

    def __init__(self, header):
        super().__init__()
        self.header = header


class KeywordHeaderRule(HeaderRule):
    def get_keywords(self) -> list:
        keywords = [
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
        ]
        return keywords

    def check(self) -> bool:
        first_word = self.header.split(" ", 1)[0]
        return first_word in self.get_keywords()

    def __str__(self):
        return f"Header of commit message should start with {self.get_keywords()}"


class MaxLengthHeaderRule(HeaderRule):
    MAX_LEN = 50

    def check(self) -> bool:
        return len(self.header) <= self.MAX_LEN

    def __str__(self):
        return (
            f"Header of commit message should be shorter than {self.MAX_LEN} characters"
        )


class DotHeaderRule(HeaderRule):
    DOT = "."

    def check(self) -> bool:
        return self.DOT not in self.header

    def __str__(self):
        return f"Header of commit message should not end with {self.DOT}"


class DesiredLengthHeaderRule(HeaderRule):
    DESIRED_LENGTH = 20

    def check(self) -> bool:
        return len(self.header) >= self.DESIRED_LENGTH

    def __str__(self):
        return f"Header of commit message should be longer than {self.DESIRED_LENGTH}"
