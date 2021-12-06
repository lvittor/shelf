# trailers = [
#     {
#         "name": "Acked-by",
#         "description": 'Owner of the affected code said "yep, looks good to me" ',
#     },
#     {
#         "name": "Bug",
#         "description": "References a bug in the Mediawiki Bugzilla installation ",
#     },
#     {"name": "CC", "description": "Person has been informed about the patch "},
#     {
#         "name": "Change-Id",
#         "description": "unique identification of a change that persists rebasing and amending ",
#     },
#     {"name": "Closes", "description": "Closes a bug"},
#     {"name": "Closes-Bug", "description": ""},
#     {"name": "Co-Authored-By", "description": ""},
#     {"name": "DocImpact", "description": ""},
#     {"name": "Git-Dch", "description": ""},
#     {"name": "Implements", "description": ""},
#     {"name": "Partial-Bug", "description": ""},
#     {"name": "Related-Bug", "description": ""},
#     {"name": "Reported-by", "description": ""},
#     {"name": "Reviewed-by", "description": ""},
#     {"name": "SecurityImpact", "description": ""},
#     {"name": "Signed-off-by", "description": ""},
#     {"name": "Suggested-by", "description": ""},
#     {"name": "Tested-by", "description": ""},
#     {"name": "Thanks", "description": ""},
#     {"name": "UpgradeImpact", "description": ""},
# ]

from ..rule import Rule


class TrailersRule(Rule):
    trailers_keyword = []
    delimiter = ":"

    def __init__(self, *args):
        super().__init__()

        for trailer in args:
            keyword = trailer.split(self.delimiter, maxsplit=1)
            trailers_keyword.append(keyword)


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
        keyword_errors = []
        for keyword in self.trailers_keyword:
            if keyword not in self.get_keywords():
                keyword_errors.append(keyword)

        return keyword_errors

    def __str__(self):
        return f"Trailers of commit message should start with {self.get_keywords()}"
