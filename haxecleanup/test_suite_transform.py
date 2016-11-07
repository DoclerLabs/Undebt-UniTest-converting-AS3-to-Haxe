# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import ZeroOrMore
from pyparsing import Optional
from pyparsing import SkipTo
from pyparsing import Combine

from undebt.pattern.common import SEMICOLON
from undebt.pattern.common import COLON
from undebt.pattern.common import LPAREN
from undebt.pattern.common import BRACES
from undebt.pattern.common import RPAREN
from undebt.pattern.common import LBRACE
from undebt.pattern.common import RBRACE
from undebt.pattern.common import NL
from undebt.pattern.common import NAME
from undebt.pattern.common import DOTTED_NAME
from undebt.pattern.util import tokens_as_dict
from undebt.pattern.util import tokens_as_list


test_suite_grammar = (
    Keyword("@Suite") + NL + Keyword("class") + NAME("classname")
)

classname = []

@tokens_as_list(assert_len=4)
def test_suite_replace(tokens):
    classname.append(tokens[3])
    return "class " + tokens[3]


constructor_grammar = (
    Keyword("public") + Keyword("function") + Keyword("new") + LPAREN + RPAREN + NL + BRACES
)

@tokens_as_list(assert_len=None)
def constructor_replace(tokens):
    return ""


public_var_grammar = (
    Optional(Combine(Literal("//") + SkipTo(Keyword("public"))))("comment") +
    Keyword("public").suppress() + Keyword("var").suppress() + NAME.suppress() + COLON.suppress() + DOTTED_NAME("class") +
    SEMICOLON.suppress()
)

classes = []

@tokens_as_dict(assert_keys_in=["class", "comment"])
def public_var_replace(tokens):
    comment = ""
    if "comment" in tokens:
        comment = tokens["comment"]
    classes.append([comment, tokens["class"]])
    return ""


classname_wrap_grammar = (
    Keyword("class") + NAME("className") +
    Optional(ZeroOrMore(NL))("nl") + LBRACE("lbrace") +
    Optional(ZeroOrMore(NL)).suppress() + RBRACE("rbrace")
)

@tokens_as_dict(assert_keys=["className", "nl", "lbrace", "rbrace"])
def classname_wrap_replace(tokens):
    arrayContent = ""
    for clas in classes:
        arrayContent += "" + clas[0] + "" + clas[1] + ",\n\t\t"

    arrayContent = arrayContent[:-4]

    return ("class " + tokens["className"] + tokens["nl"] + tokens["lbrace"] + "\n" +
            "\t@Suite('" + classname[0] + "')\n\tpublic var list:Array<Class<Dynamic>> = [\n\t\t" +
            arrayContent + 
            "\n\t];\n" +
            tokens["rbrace"])

commented_tests = []

commented_tests_grammar = (
    Literal("//") + SkipTo(NL) + NL
)

@tokens_as_list(assert_len=None)
def commented_tests_replace(tokens):
    commented_tests.append(" ".join(tokens))
    return ""


patterns = [

    # remove suite metadata from class
    (test_suite_grammar, test_suite_replace),

    # remove contructor
    (constructor_grammar, constructor_replace),

    # find all public vars
    (public_var_grammar, public_var_replace),

    # wrap into array
    (classname_wrap_grammar, classname_wrap_replace),
]
