# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import SkipTo

from undebt.pattern.common import SEMICOLON
from undebt.pattern.common import NL
from undebt.pattern.util import tokens_as_list

drop_mockolate_rule_grammar = (
    Keyword("@Rule") + NL.suppress() + SkipTo(NL) + NL.suppress()
)

@tokens_as_list(assert_len=2)
def drop_mockolate_rule_replace(tokens):
    """
    removes the mockolate rule
    """
    return ""

added_imports = []

remove_mockolate_imports_grammar = (
    Keyword("import mockolate") + SkipTo(SEMICOLON) + SEMICOLON.suppress()
)

def remove_mockolate_imports_replace(tokens):
    if(len(added_imports) == 0):
        added_imports.append(True)
        return (
            "import mockatoo.Mockatoo.*;\n"+
            "using mockatoo.Mockatoo;\n"
        )

    return ""

#----- PATTERN DEFINITION ------------------------------------------------

patterns = [

    # drop mockolate rule
    (drop_mockolate_rule_grammar, drop_mockolate_rule_replace),

    # remove mockolate imports
    (remove_mockolate_imports_grammar, remove_mockolate_imports_replace),
]
