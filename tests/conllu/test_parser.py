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

import unittest
from typing import List
from ply.yacc import LRParser
from colonel.conllu.parser import ConlluParserBuilder, IllegalTokenError, \
    IllegalEofError, IllegalMultiwordError, IllegalEmptyNodeError
from colonel.sentence import Sentence
from colonel.word import Word
from colonel.emptynode import EmptyNode
from colonel.multiword import Multiword
from colonel.upostag import UposTag


class TestConlluParserBuilder(unittest.TestCase):

    @staticmethod
    def _parse(data: str) -> List[Sentence]:
        parser = ConlluParserBuilder.build()
        return parser.parse(data)

    def test_build_returns_a_parser(self):
        self.assertIsInstance(ConlluParserBuilder.build(), LRParser)

    def test_token_error_has_expected_attributes(self):
        data = '# Foo\n' \
               '# Bar\n' \
               '\n'  # two newline after comments without sentence wordlines

        with self.assertRaises(IllegalTokenError) as err_context:
            self._parse(data)

        self.assertEqual('NEWLINE', err_context.exception.type)
        self.assertEqual('\n', err_context.exception.value)
        self.assertEqual(4, err_context.exception.line_number)
        self.assertEqual(1, err_context.exception.column_number)

    def test_eof_error(self):
        data = '# Foo\n' \
               '# Bar\n'  # following sentence wordlines are expected

        with self.assertRaises(IllegalEofError):
            self._parse(data)

    def test_one_sentence(self):
        data = '1\tFoo\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\tBar\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        result = self._parse(data)

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))

        self.assertIsInstance(result[0], Sentence)
        self.assertEqual(2, len(result[0].elements))
        self.assertEqual('Foo', result[0].elements[0].form)
        self.assertEqual('Bar', result[0].elements[1].form)

    def test_many_sentences(self):
        data = '1\tFoo\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\tBar\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n' \
               '1\tBaz\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\tQux\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        result = self._parse(data)

        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))

        self.assertIsInstance(result[0], Sentence)
        self.assertEqual(2, len(result[0].elements))
        self.assertEqual('Foo', result[0].elements[0].form)
        self.assertEqual('Bar', result[0].elements[1].form)

        self.assertIsInstance(result[1], Sentence)
        self.assertEqual(2, len(result[1].elements))
        self.assertEqual('Baz', result[1].elements[0].form)
        self.assertEqual('Qux', result[1].elements[1].form)

    def test_one_comment(self):
        data = '# Foo\n' \
               '1\tBar\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\tBaz\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        result = self._parse(data)

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))

        self.assertIsInstance(result[0], Sentence)
        self.assertEqual(2, len(result[0].elements))
        self.assertEqual('Bar', result[0].elements[0].form)
        self.assertEqual('Baz', result[0].elements[1].form)

        self.assertEqual(1, len(result[0].comments))
        self.assertEqual('Foo', result[0].comments[0])

    def test_many_comments(self):
        data = '# Foo\n' \
               '# Bar\n' \
               '1\tBaz\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\tQux\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        result = self._parse(data)

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))

        self.assertIsInstance(result[0], Sentence)
        self.assertEqual(2, len(result[0].elements))
        self.assertEqual('Baz', result[0].elements[0].form)
        self.assertEqual('Qux', result[0].elements[1].form)

        self.assertEqual(2, len(result[0].comments))
        self.assertEqual('Foo', result[0].comments[0])
        self.assertEqual('Bar', result[0].comments[1])

    def test_sentence_without_comments(self):
        data = '1\tFoo\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\tBar\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        result = self._parse(data)

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))

        self.assertIsInstance(result[0], Sentence)
        self.assertEqual(2, len(result[0].elements))
        self.assertEqual(0, len(result[0].comments))

    def test_one_word_line(self):
        data = '1\tFoo\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        result = self._parse(data)

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))

        self.assertIsInstance(result[0], Sentence)
        self.assertEqual(1, len(result[0].elements))
        self.assertIsInstance(result[0].elements[0], Word)
        self.assertEqual('Foo', result[0].elements[0].form)

    def test_sentence_with_many_word_types(self):
        data = '1-2\tFoobar\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '1\tFoo\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\tbar\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '3\t...\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '3.1\talpha\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '3.2\tbeta\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        result = self._parse(data)

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))

        self.assertIsInstance(result[0], Sentence)
        self.assertEqual(6, len(result[0].elements))

        self.assertIsInstance(result[0].elements[0], Multiword)
        self.assertEqual('Foobar', result[0].elements[0].form)

        self.assertIsInstance(result[0].elements[1], Word)
        self.assertEqual('Foo', result[0].elements[1].form)

        self.assertIsInstance(result[0].elements[2], Word)
        self.assertEqual('bar', result[0].elements[2].form)

        self.assertIsInstance(result[0].elements[3], Word)
        self.assertEqual('...', result[0].elements[3].form)

        self.assertIsInstance(result[0].elements[4], EmptyNode)
        self.assertEqual('alpha', result[0].elements[4].form)

        self.assertIsInstance(result[0].elements[5], EmptyNode)
        self.assertEqual('beta', result[0].elements[5].form)

    def test_word_with_all_attributes(self):
        data = '1\tForm\tLemma\tX\tXPOS\tA=B|C=D\t0\tDepRel\t0:X|1:Y\tMisc\n\n'

        result = self._parse(data)
        word = result[0].elements[0]
        self.assertEqual(1, word.index)
        self.assertEqual('Form', word.form)
        self.assertEqual('Lemma', word.lemma)
        self.assertEqual(UposTag.X, word.upos)
        self.assertEqual('XPOS', word.xpos)
        self.assertEqual((('A', ('B',)), ('C', ('D',))), word.feats)
        self.assertEqual(0, word.head)
        self.assertEqual('DepRel', word.deprel)
        self.assertEqual(((0, 'X'), (1, 'Y')), word.deps)
        self.assertEqual('Misc', word.misc)

    def test_word_with_no_attributes(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n\n'

        result = self._parse(data)
        word = result[0].elements[0]
        self.assertEqual(1, word.index)
        self.assertEqual('_', word.form)
        self.assertEqual('_', word.lemma)
        self.assertIsNone(word.upos)
        self.assertIsNone(word.xpos)
        self.assertIsNone(word.feats)
        self.assertIsNone(word.head)
        self.assertIsNone(word.deprel)
        self.assertIsNone(word.deps)
        self.assertIsNone(word.misc)

    def test_emptynode_with_all_attributes(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2.1\tForm\tLemma\tX\tXPOS\tA=B|C=D\t_\t_\t0:X|1:Y\tMisc\n' \
               '\n'

        result = self._parse(data)
        word = result[0].elements[2]
        self.assertEqual(2, word.main_index)
        self.assertEqual(1, word.sub_index)
        self.assertEqual('Form', word.form)
        self.assertEqual('Lemma', word.lemma)
        self.assertEqual(UposTag.X, word.upos)
        self.assertEqual('XPOS', word.xpos)
        self.assertEqual((('A', ('B',)), ('C', ('D',))), word.feats)
        self.assertEqual(((0, 'X'), (1, 'Y')), word.deps)
        self.assertEqual('Misc', word.misc)

    def test_emptynode_with_no_attributes(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2.1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        result = self._parse(data)
        word = result[0].elements[2]
        self.assertEqual(2, word.main_index)
        self.assertEqual(1, word.sub_index)
        self.assertEqual('_', word.form)
        self.assertEqual('_', word.lemma)
        self.assertIsNone(word.upos)
        self.assertIsNone(word.xpos)
        self.assertIsNone(word.feats)
        self.assertIsNone(word.deps)
        self.assertIsNone(word.misc)

    def test_error_if_emptynode_has_head(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2.1\tForm\tLemma\tX\tXPOS\tA=B|C=D\t0\t_\t0:X|1:Y\tMisc\n' \
               '\n'

        with self.assertRaises(IllegalEmptyNodeError) as err_context:
            self._parse(data)

        self.assertEqual(3, err_context.exception.line_number)

    def test_error_if_emptynode_has_deprel(self):
        data = \
            '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
            '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
            '2.1\tForm\tLemma\tX\tXPOS\tA=B|C=D\t_\tDepRel\t0:X|1:Y\tMisc\n' \
            '\n'

        with self.assertRaises(IllegalEmptyNodeError) as err_context:
            self._parse(data)

        self.assertEqual(3, err_context.exception.line_number)

    def test_multiword_with_all_attributes(self):
        data = '1-2\tForm\t_\t_\t_\t_\t_\t_\t_\tMisc\n' \
               '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        result = self._parse(data)
        word = result[0].elements[0]
        self.assertEqual(1, word.first_index)
        self.assertEqual(2, word.last_index)
        self.assertEqual('Form', word.form)
        self.assertEqual('Misc', word.misc)

    def test_multiword_with_no_attributes(self):
        data = '1-2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        result = self._parse(data)
        word = result[0].elements[0]
        self.assertEqual(1, word.first_index)
        self.assertEqual(2, word.last_index)
        self.assertEqual('_', word.form)
        self.assertIsNone(word.misc)

    def test_error_if_multiword_has_lemma(self):
        data = '1-2\tForm\tLemma\t_\t_\t_\t_\t_\t_\tMisc\n' \
               '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        with self.assertRaises(IllegalMultiwordError) as err_context:
            self._parse(data)

        self.assertEqual(1, err_context.exception.line_number)

    def test_error_if_multiword_has_upos(self):
        data = '1-2\tForm\t_\tX\t_\t_\t_\t_\t_\tMisc\n' \
               '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        with self.assertRaises(IllegalMultiwordError) as err_context:
            self._parse(data)

        self.assertEqual(1, err_context.exception.line_number)

    def test_error_if_multiword_has_xpos(self):
        data = '1-2\tForm\t_\t_\tXPOS\t_\t_\t_\t_\tMisc\n' \
               '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        with self.assertRaises(IllegalMultiwordError) as err_context:
            self._parse(data)

        self.assertEqual(1, err_context.exception.line_number)

    def test_error_if_multiword_has_feats(self):
        data = '1-2\tForm\t_\t_\t_\tA=B\t_\t_\t_\tMisc\n' \
               '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        with self.assertRaises(IllegalMultiwordError) as err_context:
            self._parse(data)

        self.assertEqual(1, err_context.exception.line_number)

    def test_error_if_multiword_has_head(self):
        data = '1-2\tForm\t_\t_\t_\t_\t0\t_\t_\tMisc\n' \
               '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        with self.assertRaises(IllegalMultiwordError) as err_context:
            self._parse(data)

        self.assertEqual(1, err_context.exception.line_number)

    def test_error_if_multiword_has_deprel(self):
        data = '1-2\tForm\t_\t_\t_\t_\t_\tDepRel\t_\tMisc\n' \
               '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        with self.assertRaises(IllegalMultiwordError) as err_context:
            self._parse(data)

        self.assertEqual(1, err_context.exception.line_number)

    def test_error_if_multiword_has_deps(self):
        data = '1-2\tForm\t_\t_\t_\t_\t_\t_\t0:X\tMisc\n' \
               '1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
               '\n'

        with self.assertRaises(IllegalMultiwordError) as err_context:
            self._parse(data)

        self.assertEqual(1, err_context.exception.line_number)
