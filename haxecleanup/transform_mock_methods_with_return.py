# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import Optional
from pyparsing import SkipTo
from pyparsing import Combine

from undebt.pattern.common import DOT
from undebt.pattern.common import SEMICOLON
from undebt.pattern.common import LPAREN
from undebt.pattern.common import RPAREN
from undebt.pattern.util import tokens_as_dict

from undebt.haxecleanup.common import mock_usage_what_grammar
from undebt.haxecleanup.common import get_verify_replace


# mock methods
mock_methods_grammar = (
    mock_usage_what_grammar +
    DOT +
    Keyword("method") + LPAREN + Literal('"') + SkipTo(Literal('"'))("methodName") + Literal('"') + RPAREN +
    DOT +
    Optional(Combine(Keyword("noArgs") + LPAREN + RPAREN + DOT))("noargs") +
    Optional(Combine(Keyword("anyArgs") + LPAREN + RPAREN + DOT))("anyargs") +
    Keyword("returns") + LPAREN + SkipTo(RPAREN)("returns") + RPAREN +
    DOT +
    Optional(Combine(Keyword("noArgs") + LPAREN + RPAREN + DOT)) +
    SkipTo(SEMICOLON)("verify")
)

@tokens_as_dict(assert_keys_in=["what", "methodName", "returns", "verify", "noargs", "anyargs"])
def mock_methods_replace(tokens):
    args = ""
    if "anyargs" in tokens:
        args = "cast any"

    verify = get_verify_replace(tokens["verify"])
    if verify == "":
        return None

    return tokens["what"] + "." + tokens["methodName"] + "(" + args + ").returns(" + tokens["returns"] +")." + verify


patterns = [

    # replace mock usages
    (mock_methods_grammar, mock_methods_replace), 

]
