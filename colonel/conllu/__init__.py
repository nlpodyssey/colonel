# Copyright 2018 The NLP Odyssey Authors.
# Copyright 2018 Marco Nicola <marconicola@disroot.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This package provides modules to process *CoNLL-U* formatted string,
providing a lexical analyzer (see :mod:`.lexer`) and a parser (see
:mod:`.parser`) to transform the raw string input into related
:class:`.Sentence` objects.

Lexer and parser classes are implemented taking advantage of the *PLY
(Python Lex-Yacc)* library; you can learn more from the
`PLY documentation <http://www.dabeaz.com/ply>`_ and from the
`Lex & Yacc Page <http://dinosaur.compilertools.net/>`_.
"""

from typing import List
from colonel.sentence import Sentence
from colonel.conllu.parser import ConlluParserBuilder


def parse(content: str) -> List[Sentence]:
    """Parses a *CoNLL-U* string content, returning a list of sentences.

    :raise lexer.LexerError: (any specific subclass) in case of invalid input
        breaking the rules of the *CoNLL-U* lexer
    :raise parser.ParserError: (any specific subclass) in case of invalid input
        breaking the rules of the *CoNLL-U* parser

    :param content: *CoNLL-U* formatted string to be parsed
    :return: list of parsed :class:`.Sentence` items
    """
    return ConlluParserBuilder.build().parse(content)
