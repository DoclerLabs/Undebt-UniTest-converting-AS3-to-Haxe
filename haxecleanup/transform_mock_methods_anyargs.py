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
    Keyword("anyArgs") + LPAREN + RPAREN +
    Optional(Combine(DOT + SkipTo(SEMICOLON)("verify"))) + SEMICOLON
)

@tokens_as_dict(assert_keys_in=["what", "methodName", "verify"])
def mock_methods_replace(tokens):
    verify = ""
    if "verify" in tokens:
        verify = get_verify_replace(tokens["verify"])
        if verify == "":
            return None
        else: verify = "." + verify

    return tokens["what"] + "." + tokens["methodName"] + "(" + "cast any" + ")" + verify + ";"


patterns = [

    # replace mock usages
    (mock_methods_grammar, mock_methods_replace), 

]
