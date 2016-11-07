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


# mock methods
mock_methods_grammar = (
    mock_usage_what_grammar +
    DOT +
    Keyword("method") + LPAREN + Literal('"') + SkipTo(Literal('"'))("methodName") + Literal('"') + RPAREN +
    DOT +
    Optional(Combine(Keyword("noArgs") + LPAREN + RPAREN + DOT)) +
    Keyword("returns") + LPAREN + SkipTo(RPAREN)("returns") + RPAREN + SEMICOLON
)

@tokens_as_dict(assert_keys=["what", "methodName", "returns"])
def mock_methods_replace(tokens):
    """
    mock(something).method("someMethod").returns(someValue);
    - OR -
    mock(something).method("someMethod").noArgs().returns(someValue);
    ->
    something.someMethod().returns(someValue);
    """
    return tokens["what"] + "." + tokens["methodName"] + "().returns(" + tokens["returns"] +");"


patterns = [

    # replace mock usages
    (mock_methods_grammar, mock_methods_replace), 

]
