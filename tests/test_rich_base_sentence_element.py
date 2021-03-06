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
from colonel.base_rich_sentence_element import BaseRichSentenceElement
from colonel.upostag import UposTag


class TestBaseRichSentenceElement(unittest.TestCase):

    def test_init_form(self):
        element = BaseRichSentenceElement(form='Foo')
        self.assertEqual('Foo', element.form)

    def test_init_lemma(self):
        element = BaseRichSentenceElement(lemma='Foo')
        self.assertEqual('Foo', element.lemma)

    def test_init_upos(self):
        element = BaseRichSentenceElement(upos=UposTag.X)
        self.assertEqual(UposTag.X, element.upos)

    def test_init_xpos(self):
        element = BaseRichSentenceElement(xpos='Foo')
        self.assertEqual('Foo', element.xpos)

    def test_init_feats(self):
        element = BaseRichSentenceElement(feats={'foo': 'bar'})
        self.assertEqual({'foo': 'bar'}, element.feats)

    def test_init_deps(self):
        element = BaseRichSentenceElement(deps={'foo': 'bar'})
        self.assertEqual({'foo': 'bar'}, element.deps)

    def test_init_misc(self):
        element = BaseRichSentenceElement(misc='Foo')
        self.assertEqual('Foo', element.misc)

    def test_is_valid_true_with_no_values_set(self):
        element = BaseRichSentenceElement()
        self.assertTrue(element.is_valid())

    def test_is_valid_true_with_all_values_set(self):
        element = BaseRichSentenceElement(
            form='Form',
            lemma='Lemma',
            upos=UposTag.X,
            xpos='XPOS',
            feats={'foo': 'bar'},
            deps={'baz': 'qux'},
            misc='Misc'
        )
        self.assertTrue(element.is_valid())

    def test_to_conllu_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            BaseRichSentenceElement().to_conllu()
