# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import SkipTo

from undebt.cmd.logger import log

from undebt.pattern.common import LPAREN
from undebt.pattern.common import RPAREN
from undebt.pattern.common import LBRACE
from undebt.pattern.common import RBRACE
from undebt.pattern.common import INDENT


mock_usage_what_grammar = (
    Keyword("mock") + LPAREN + SkipTo(RPAREN)("what") + RPAREN
)

before_grammar = (
    Keyword("@Before")("before") + SkipTo(LBRACE)("head") + LBRACE("lbrace") + INDENT("indent") + SkipTo(RBRACE)("body") + RBRACE("rbrace")
)

after_grammar = (
    Keyword("@After")("after") + SkipTo(LBRACE)("head") + LBRACE("lbrace") + INDENT("indent") + SkipTo(RBRACE)("body") + RBRACE("rbrace")
)


def add_mocks_to_before(tokens, mocked_things):
    """
    Assigns mocked classes to their variables
    """

    # add initialization of all mocks
    mockInit = ""
    for mock in mocked_things:
        mockInit += tokens["indent"] + "this." + mock["name"] + " = mock(" + mock["type"] + ");"

    return (tokens["before"] +
            tokens["head"] +
            tokens["lbrace"] +
            mockInit + "\n" +
            tokens["indent"] + tokens["body"] +
            tokens["rbrace"])


def get_verify_replace(token):
    verify = ""
    log.info(token)
    if token == "once()":
        verify = "verify()"
    if token == "never()":
        verify = "verify(never)"

    token_split = token.split("(")
    if token_split[0] == "atLeast":
        verify = "verify(" + token + ")"
    if token_split[0] == "atMost":
        verify = "verify(" + token + ")"

    return verify
