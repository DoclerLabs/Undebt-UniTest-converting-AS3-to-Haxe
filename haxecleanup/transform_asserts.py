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
from undebt.pattern.common import PARENS
from undebt.pattern.common import NL
from undebt.pattern.common import NAME
from undebt.pattern.util import tokens_as_dict


import_assert_grammar = (
    Keyword("import") +
    Optional(NAME + DOT)("importBegin") +
    Literal("flexunit")("flexunit") +
    SkipTo(SEMICOLON)("importEnd") + SEMICOLON + NL
)

import_replaced = []

@tokens_as_dict(assert_keys_in=["importBegin", "flexunit", "importEnd"])
def import_assert_replace(tokens):
    if("assert" not in tokens["importEnd"].lower()):
        return None
    if(len(import_replaced) == 0):
        import_replaced.append(True)
        return ("import hex.unittest.assertion.Assert;\n")
    return ""


replace_assert_grammar = (
    Keyword("Assert")("assert") + DOT + NAME("assertType") + PARENS("assertion")
)


@tokens_as_dict(assert_keys=["assert", "assertType", "assertion"])
def replace_assert_replace(tokens):
    assertType = ""
    if(tokens["assertType"] == "assertEquals" or tokens["assertType"] == "areEqual"):
        assertType = "equals"
    if(tokens["assertType"] == "assertTrue" or tokens["assertType"] == "isTrue"):
        assertType = "isTrue"
    if(tokens["assertType"] == "assertFalse" or tokens["assertType"] == "isFalse"):
        assertType = "isFalse"
    if(tokens["assertType"] == "assertNull" or tokens["assertType"] == "isNull"):
        assertType = "isNull"
    if(tokens["assertType"] == "assertNotNull" or tokens["assertType"] == "isNotNull"):
        assertType = "isNotNull"

    if(assertType == ""):
        return None
    
    return tokens["assert"] + "." + assertType + tokens["assertion"]


patterns = [
    # replace import for assert
    (import_assert_grammar, import_assert_replace),

    # replace Asserts (simple string to string)
    (replace_assert_grammar, replace_assert_replace)
]
