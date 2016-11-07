# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import SkipTo

from undebt.pattern.common import PARENS
from undebt.pattern.common import LBRACE
from undebt.pattern.common import RBRACE
from undebt.pattern.common import NL
from undebt.pattern.common import NAME
from undebt.pattern.util import tokens_as_dict
from undebt.pattern.util import tokens_as_list

from undebt.haxecleanup.common import before_grammar
from undebt.haxecleanup.common import after_grammar

extends_drop_grammar = (
    Keyword("class").suppress() + NAME + Keyword("extends").suppress() + Keyword("TestCase").suppress()
)

extends_test_case = []


@tokens_as_list(assert_len_in=[1])
def extends_drop_replace(tokens):
    """
    class <NAME> extends TestCase
    ->
    class <NAME>
    """
    if(len(tokens) == 0):
        return None

    extends_test_case.append(True)
    return (
        "class " + tokens[0]
    )


super_call_drop_grammar = (
    Literal("public function new") + PARENS + SkipTo(LBRACE) + LBRACE + SkipTo(RBRACE) + RBRACE
)


@tokens_as_list(assert_len=6)
def super_call_drop_replace(tokens):

    """
    public function new()
    {
        super();
    }
    ->
    public function new()
    {
    }
    """
    if(not was_test_case()):
        return None

    expressions = tokens[4].split("\n")
    finalExpressions = []
    for exp in expressions:
        if("super" not in exp):
            finalExpressions.append(exp)

    return tokens[0] + tokens[1] + tokens[2] + tokens[3] + "\n".join(finalExpressions) + tokens[5]


@tokens_as_dict(assert_keys=["before", "head", "lbrace", "body", "rbrace", "indent"])
def remove_override_from_before(tokens):
    # remove override if previously extending from TestCase
    tokens["head"] = remove_override_from_function(tokens["head"])

    return (tokens["before"] +
            tokens["head"] +
            tokens["lbrace"] +
            tokens["indent"] + tokens["body"] +
            tokens["rbrace"])


@tokens_as_dict(assert_keys=["after", "head", "lbrace", "body", "rbrace", "indent"])
def remove_override_from_after(tokens):

    # remove override if previously extending from TestCase
    tokens["head"] = remove_override_from_function(tokens["head"])

    return (tokens["after"] +
            tokens["head"] +
            tokens["lbrace"] +
            tokens["indent"] + tokens["body"] +
            tokens["rbrace"])


test_case_import_grammar = (
    Literal("import flexunit.framework.TestCase;") 
)

@tokens_as_list(assert_len=1)
def test_case_import_replace(tokens):
    return ""

#---- UTILS --------------------------------------------------------------

def remove_override_from_function(function_header):
    if(was_test_case()):
        head = function_header.split(" ")
        finalHead = []
        for word in head:
            if("override" not in word):
                finalHead.append(word)
        return " ".join(finalHead)
    return function_header

def was_test_case():
    return len(extends_test_case) > 0

patterns = [
    # remove extends
    (extends_drop_grammar, extends_drop_replace),

    # remove super call
    (super_call_drop_grammar, super_call_drop_replace),

    # remove override from @Before
    (before_grammar, remove_override_from_before),

    # remove override from @After
    (after_grammar, remove_override_from_after),

    # remove import for TestCase
    (test_case_import_grammar, test_case_import_replace),

]
