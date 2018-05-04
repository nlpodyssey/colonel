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
from unittest.mock import patch, Mock

from colonel.conllu import parse, to_conllu
from colonel.conllu.parser import ConlluParserBuilder
from colonel.sentence import Sentence


class TestConlluModule(unittest.TestCase):

    def test_parse_builds_a_parser_and_returns_its_parsed_result(self):
        content = 'foo'  # The input content
        result = Mock()  # The expected final result

        parser = Mock()  # The parser built by ConlluParserBuilder
        parser.parse = Mock(return_value=result)

        with patch.object(ConlluParserBuilder, 'build', return_value=parser):
            actual_result = parse(content)

        parser.parse.assert_called_once_with(content)
        self.assertIs(result, actual_result)

    def test_to_conllu_with_empty_array(self):
        self.assertEqual('', to_conllu([]))

    def test_to_conllu_with_one_sentence(self):
        sentences = [
            FakeSentence('Foo\n')
        ]

        self.assertEqual('Foo\n', to_conllu(sentences))

    def test_to_conllu_with_meny_sentences(self):
        sentences = [
            FakeSentence('Foo\n'),
            FakeSentence('Bar\n'),
            FakeSentence('Baz\n')
        ]

        expected = 'Foo\nBar\nBaz\n'
        self.assertEqual(expected, to_conllu(sentences))


class FakeSentence(Sentence):
    def __init__(self, fake_conllu):
        super(FakeSentence, self).__init__()
        self._fake_conllu = fake_conllu

    def to_conllu(self):
        return self._fake_conllu
