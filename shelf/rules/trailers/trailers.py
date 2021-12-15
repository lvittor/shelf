from ..rule import Rule


class TrailersRule(Rule):
    trailers_key = []
    DELIMITER = ":"

    def __init__(self, trailers: list):
        super().__init__()
        if trailers:
            for trailer in trailers:
                key, value = trailer
                self.trailers_key.append(key)

class KeywordTrailersRule(TrailersRule):
    def get_keywords(self) -> list:
        keywords = [
            "Acked-by",
            "Bug",
            "CC",
            "Change-Id",
            "Closes-Bug",
            "Co-Authored-By",
            "DocImpact",
            "Git-Dch",
            "Implements",
            "Partial-Bug",
            "Related-Bug",
            "Reported-by",
            "Reviewed-by",
            "SecurityImpact",
            "Signed-off-by",
            "Suggested-by",
            "Tested-by",
            "Thanks",
            "UpgradeImpact",
        ]
        return keywords

    def check(self) -> list:
        for keyword in self.trailers_key:
            if keyword not in self.get_keywords():
                return False
        return True

    def __str__(self):
        return f"Trailers of commit message should start with {self.get_keywords()}"
