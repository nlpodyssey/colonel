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
from colonel.word import Word
from colonel.upostag import UposTag


class TestWord(unittest.TestCase):

    def test_init_index(self):
        element = Word(index=42)
        self.assertEqual(42, element.index)

    def test_init_form(self):
        element = Word(form='Foo')
        self.assertEqual('Foo', element.form)

    def test_init_lemma(self):
        element = Word(lemma='Foo')
        self.assertEqual('Foo', element.lemma)

    def test_init_upos(self):
        element = Word(upos=UposTag.X)
        self.assertEqual(UposTag.X, element.upos)

    def test_init_xpos(self):
        element = Word(xpos='Foo')
        self.assertEqual('Foo', element.xpos)

    def test_init_feats(self):
        element = Word(feats={'foo': 'bar'})
        self.assertEqual({'foo': 'bar'}, element.feats)

    def test_init_head(self):
        element = Word(head=42)
        self.assertEqual(42, element.head)

    def test_init_deprel(self):
        element = Word(deprel='Foo')
        self.assertEqual('Foo', element.deprel)

    def test_init_deps(self):
        element = Word(deps={'foo': 'bar'})
        self.assertEqual({'foo': 'bar'}, element.deps)

    def test_init_misc(self):
        element = Word(misc='Foo')
        self.assertEqual('Foo', element.misc)

    def test_is_valid_false_with_no_values_set(self):
        element = Word()
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_index_less_than_zero(self):
        element = Word(index=-1)
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_index_equal_to_zero(self):
        element = Word(index=0)
        self.assertFalse(element.is_valid())

    def test_is_valid_true_with_index_greater_than_zero(self):
        element = Word(index=1)
        self.assertTrue(element.is_valid())

    def test_is_valid_true_with_all_values_set(self):
        element = Word(
                index=1,
                form='Form',
                lemma='Lemma',
                upos=UposTag.X,
                xpos='XPOS',
                feats={'foo': 'bar'},
                head=2,
                deprel='DepRel',
                misc='Misc',
                deps={'baz': 'qux'}
        )
        self.assertTrue(element.is_valid())
