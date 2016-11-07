# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Literal

from undebt.pattern.common import SEMICOLON
from undebt.pattern.common import NL
from undebt.pattern.common import NAME

from undebt.pattern.util import tokens_as_dict

from undebt.haxecleanup.common import before_grammar
from undebt.haxecleanup.common import add_mocks_to_before


mock_definition = (
    Keyword("@Mock") + NL.suppress() +
    Keyword("public").suppress() + Keyword("var").suppress() +
    NAME("name") + Literal(":").suppress() + NAME("type") + SEMICOLON.suppress()  
)

mocked_things = []

@tokens_as_dict(assert_keys=["name", "type"])
def store_mocks(tokens):
    """
    @Mock
    public var something:SomeType;
    ->
    private var something:SomeType;
    """

    mocked_things.append(tokens)
    return "private var " + tokens["name"] + " : " + tokens["type"] + ";"


@tokens_as_dict(assert_keys=["before", "head", "lbrace", "body", "rbrace", "indent"])
def process_before(tokens):
    """
    @Before
    public function before()
    {
        this.something = mock(SomeType);

        ... etc
    }
    """
    return add_mocks_to_before(tokens, mocked_things)


patterns = [

    # find mock definitions and store them
    (mock_definition, store_mocks),

    # process the @Before function
    (before_grammar, process_before),

]
