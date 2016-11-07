# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Literal

from undebt.pattern.common import LPAREN
from undebt.pattern.common import RPAREN
from undebt.pattern.common import NAME
from undebt.pattern.common import INDENT
from undebt.pattern.util import tokens_as_dict

# mock getters
dataprovider_test_grammar = (
    INDENT("indent") +
    Keyword("@Test")("test") +
    LPAREN.suppress() +
    Keyword("dataProvider").suppress() +
    Literal("=").suppress() + Literal('"').suppress() + NAME("name") + Literal('"').suppress() +
    RPAREN.suppress()
)

@tokens_as_dict(assert_keys=["indent", "test", "name"])
def dataprovider_test_replace(tokens):    
    '''
    @Test(dataprovider="someDataProvider")
    ->
    @Test
    @DataProvider("someDataProvider")
    '''
    return (tokens["indent"] + tokens["test"] + "" +
            tokens["indent"] + '@DataProvider("' + tokens["name"] + '")')


patterns = [

    # replace dataprovider tests
    (dataprovider_test_grammar, dataprovider_test_replace),

]
