# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Literal

from undebt.pattern.common import LPAREN
from undebt.pattern.common import PARENS
from undebt.pattern.common import RPAREN
from undebt.pattern.common import NL
from undebt.pattern.common import NAME
from undebt.pattern.util import tokens_as_list

as3_to_hx_meta_grammar = (
    Literal("@:meta").suppress() + LPAREN.suppress() + NAME + RPAREN.suppress() + NL.suppress()
)


@tokens_as_list(assert_len=1)
def as3_to_hx_meta_replace(tokens):
    """
    @:meta(Before())
    ->
    @Before()
    """
    meta = tokens[0]
    return (
        "@"+meta
    )


parens_drop_grammar = (
    Literal("@") + NAME + Literal("()").suppress()
)


@tokens_as_list(assert_len=2)
def parens_drop_replace(tokens):
    """
    @Before()
    ->
    @Before
    """
    #meta = tokens[0]
    return (
        tokens[0] + tokens[1]
    )


runwith_drop_grammar = (
    Keyword("@RunWith").suppress() + PARENS("runner") + NL.suppress()
)


@tokens_as_list(assert_len=1)
def runwith_drop_replace(tokens):
    """
    removes RunWith() metadata
    """
    return ""

patterns = [
    # convert metadata to proper haxe annotations 
    (as3_to_hx_meta_grammar, as3_to_hx_meta_replace),

    # drop parentesis after metadata that are not defining anything
    (parens_drop_grammar, parens_drop_replace),
    
    # remove RunWith
    (runwith_drop_grammar, runwith_drop_replace),

]
