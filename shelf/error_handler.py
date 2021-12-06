from rules.header.header import (
    DesiredLengthHeaderRule,
    DotHeaderRule,
    KeywordHeaderRule,
    MaxLengthHeaderRule,
)

from rules.trailers.trailers import (
    KeywordTrailersRule
) 

from rules.body.body import (
    MaxLengthBodyRule,
    MinLengthBodyRule,
    TrailingWhitespaceBodyRule,
    HardTabBodyRule,
    BodyMissingBodyRule
)

from sh import git


class ErrorHandler:
    header_rules = [
        KeywordHeaderRule,
        MaxLengthHeaderRule,
        DotHeaderRule,
        DesiredLengthHeaderRule,
    ]

    trailers_rules = [
        KeywordTrailersRule
    ]

    body_rules = [
        MaxLengthBodyRule,
        MinLengthBodyRule,
        TrailingWhitespaceBodyRule,
        HardTabBodyRule,
        BodyMissingBodyRule
    ]

    @classmethod
    def get_header(cls, commit_msg):
        return commit_msg.split("\n")[0]

    @classmethod
    def get_trailers(cls, commit_msg):
        # str_trailers = "" # echo "commit_msg" | git interpret-trailers --only-trailers
        # line_trailers = str_trailers.split("\n")
        # keywords = []
        # for trailer in line_trailers:
        #     keywords.append(trailer.split(":"))
        # return keywords
        pass 
    
    @classmethod
    def get_body(cls, commit_msg):
        pass 


    @classmethod
    def check_commit_msg(cls, commit_msg):
        errors = []
        errors.extend(cls.check_header(header=get_header(commit_msg))
        #errors.extend(cls.check_trailers(trailers=get_trailers(commit_msg)))
        #errors.extend(cls.check_body(body=get_body(commit_msg)))
        return errors

    @classmethod
    def check_header(cls, header):
        errors = []
        for rule in cls.header_rules:
            current_rule = rule(header)
            if not current_rule.check():
                errors.append(current_rule)

        return errors

    @classmethod
    def check_trailers(cls, trailers):
        errors = []
        for rule in cls.trailers_rules:
            current_rule = rule(trailers)
            if not current_rule.check():
                errors.append(current_rule)

        return erros

    @classmethod
    def check_body(cls, body):
        errors = []
        for rule in cls.body_rules:
            current_rule = rule(body)
            if not current_rule.check():
                errors.append(current_rule)