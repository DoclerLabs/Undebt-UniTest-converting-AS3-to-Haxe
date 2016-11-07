# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import Optional
from pyparsing import SkipTo

from undebt.pattern.common import DOT
from undebt.pattern.common import SEMICOLON
from undebt.pattern.common import LPAREN
from undebt.pattern.common import RPAREN
from undebt.pattern.util import tokens_as_dict

from undebt.haxecleanup.common import mock_usage_what_grammar
from undebt.haxecleanup.common import get_verify_replace


# mock getters
mock_getters_grammar = (
    mock_usage_what_grammar +
    DOT +
    Keyword("getter") + LPAREN + Literal('"') + SkipTo(Literal('"'))("getterName") + Literal('"') + RPAREN +
    DOT +
    Keyword("returns") + LPAREN + SkipTo(RPAREN)("returnValues") + RPAREN +
    Optional(DOT + SkipTo(SEMICOLON)("verify"))
    + SEMICOLON
)

@tokens_as_dict(assert_keys_in=["what", "getterName", "returnValues", "verify"])
def mock_getters_replace(tokens):
    verify = ""
    if("verify" in tokens):
        verify = get_verify_replace(tokens["verify"])
        if verify == "":
            return None
    
    if(verify != ""):
        verify = "." + verify

    return tokens["what"] + "." + tokens["getterName"] + ".returns(" + tokens["returnValues"] + ")" + verify + ";"



patterns = [

    # replace mock usages
    (mock_getters_grammar, mock_getters_replace),

]
