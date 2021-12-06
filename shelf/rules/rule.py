class Rule:
    def __init__(self, code=None, name=None, description=None, color=None):
        self.code = code
        self.name = name
        self.description = description
        self.color = color

    def check(self):
        raise NotImplementedError

    def show_errors(self):
        raise NotImplementedError

    def __eq__(self, other):
        return isinstance(other, Rule) and self.id == other.id

    def __str__(self):
        return f"{self.code} {self.name}"
