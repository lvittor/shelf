import subprocess

from rules.body.body import (
    BodyMissingBodyRule,
    HardTabBodyRule,
    MaxLengthBodyRule,
    MinLengthBodyRule,
    TrailingWhitespaceBodyRule,
)
from rules.header.header import (
    DesiredLengthHeaderRule,
    DotHeaderRule,
    KeywordHeaderRule,
    MaxLengthHeaderRule,
)
from rules.trailers.trailers import KeywordTrailersRule


class ErrorHandler:
    header_rules = [
        KeywordHeaderRule,
        MaxLengthHeaderRule,
        DotHeaderRule,
        DesiredLengthHeaderRule,
    ]

    trailers_rules = [KeywordTrailersRule]

    body_rules = [
        MaxLengthBodyRule,
        MinLengthBodyRule,
        TrailingWhitespaceBodyRule,
        HardTabBodyRule,
        BodyMissingBodyRule,
    ]

    @classmethod
    def get_header(cls, commit_msg: str):
        return commit_msg.split("\n")[0]

    @classmethod
    def get_trailers(cls, commit_msg: str):
        str_trailers = subprocess.check_output(
            ["git", "interpret-trailers", "--only-trailers"],
            input=f"{commit_msg}",
            text=True,
        ).strip()
        if not str_trailers:
            return [], []
        trailers = str_trailers.split("\n")
        trailers_key_val = []
        for trailer in trailers:
            trailers_key_val.append(trailer.split(":", maxsplit=1))
        return trailers_key_val, trailers

    @classmethod
    def get_body(cls, commit_msg: str, trailers: str):
        try:
            body_and_trailers = commit_msg.split("\n", 2)[2]
        except:
            return []
        body_lines = []
        for line in body_and_trailers.split("\n"):
            if line not in trailers:
                body_lines.append(line)
        return body_lines

    @classmethod
    def check_commit_msg(cls, commit_msg):
        errors = []
        errors.extend(
            cls.check_errors(rules=cls.header_rules, words=cls.get_header(commit_msg))
        )
        trailers_key_val, trailers = cls.get_trailers(commit_msg)
        errors.extend(
            cls.check_errors(rules=cls.trailers_rules, words=trailers_key_val)
        )
        errors.extend(
            cls.check_errors(
                rules=cls.body_rules, words=cls.get_body(commit_msg, trailers)
            )
        )
        return errors

    @classmethod
    def check_errors(cls, rules: list, words: list):
        errors = []
        for rule in rules:
            current_rule = rule(words)
            if not current_rule.check():
                errors.append(current_rule)
        return errors
