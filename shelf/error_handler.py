from rules.header.header import (
    DesiredLengthHeaderRule,
    DotHeaderRule,
    KeywordHeaderRule,
    MaxLengthHeaderRule,
)


class ErrorHandler:
    header_rules = [
        KeywordHeaderRule,
        MaxLengthHeaderRule,
        DotHeaderRule,
        DesiredLengthHeaderRule,
    ]

    @classmethod
    def check_commit_msg(cls, commit_msg):
        errors = []
        errors.extend(cls.check_header(header=commit_msg.split("\n")[0]))
        return errors

    @classmethod
    def check_header(cls, header):
        errors = []
        for rule in cls.header_rules:
            current_rule = rule(header)
            if not current_rule.check():
                errors.append(current_rule)

        return errors
