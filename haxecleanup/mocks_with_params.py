# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Literal

from undebt.pattern.common import SEMICOLON
from undebt.pattern.common import PARENS
from undebt.pattern.common import NL
from undebt.pattern.common import NAME
from undebt.pattern.util import tokens_as_dict

from undebt.haxecleanup.common import before_grammar
from undebt.haxecleanup.common import add_mocks_to_before


mock_definition = (
    Keyword("@Mock") + PARENS("mockType") + NL.suppress() +
    Keyword("public").suppress() + Keyword("var").suppress() +
    NAME("name") + Literal(":").suppress() + NAME("type") + SEMICOLON.suppress()  
)

mocked_things = []

@tokens_as_dict(assert_keys=["name", "type", "mockType"])
def store_mocks(tokens):
    """
    reads all the mocked classes and stores them for later processing
    """

    mocked_things.append(tokens)
    return "private var " + tokens["name"] + " : " + tokens["type"] + ";"


@tokens_as_dict(assert_keys=["before", "head", "lbrace", "body", "rbrace", "indent"])
def process_before(tokens):
    return add_mocks_to_before(tokens, mocked_things)

patterns = [

    # find mock definitions and store them
    (mock_definition, store_mocks),

    # process the @Before function
    (before_grammar, process_before),

]
