from utils import get_git_directory

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
        import yaml

        with open(f"{get_git_directory()}/shelf.yml", "r") as f:
            doc = yaml.load(f, Loader=yaml.FullLoader)
        keywords = doc["trailers"]
        return keywords

    def check(self) -> list:
        for keyword in self.trailers_key:
            if keyword not in self.get_keywords():
                return False
        return True

    def __str__(self):
        return f"Trailers of commit message should start with {self.get_keywords()}"
