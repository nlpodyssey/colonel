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
from colonel.emptynode import EmptyNode
from colonel.upostag import UposTag


class TestEmptyNode(unittest.TestCase):

    def test_init_main_index(self):
        element = EmptyNode(main_index=42)
        self.assertEqual(42, element.main_index)

    def test_init_sub_index(self):
        element = EmptyNode(sub_index=42)
        self.assertEqual(42, element.sub_index)

    def test_init_form(self):
        element = EmptyNode(form='Foo')
        self.assertEqual('Foo', element.form)

    def test_init_lemma(self):
        element = EmptyNode(lemma='Foo')
        self.assertEqual('Foo', element.lemma)

    def test_init_upos(self):
        element = EmptyNode(upos=UposTag.X)
        self.assertEqual(UposTag.X, element.upos)

    def test_init_xpos(self):
        element = EmptyNode(xpos='Foo')
        self.assertEqual('Foo', element.xpos)

    def test_init_feats(self):
        element = EmptyNode(feats={'foo': 'bar'})
        self.assertEqual({'foo': 'bar'}, element.feats)

    def test_init_deps(self):
        element = EmptyNode(deps={'foo': 'bar'})
        self.assertEqual({'foo': 'bar'}, element.deps)

    def test_init_misc(self):
        element = EmptyNode(misc='Foo')
        self.assertEqual('Foo', element.misc)

    def test_is_valid_false_with_no_values_set(self):
        element = EmptyNode()
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_main_index_is_not_set(self):
        element = EmptyNode(sub_index=42)
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_sub_index_is_not_set(self):
        element = EmptyNode(main_index=42)
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_main_index_less_than_zero(self):
        element = EmptyNode(main_index=-1, sub_index=42)
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_sub_index_less_than_zero(self):
        element = EmptyNode(main_index=42, sub_index=-1)
        self.assertFalse(element.is_valid())

    def test_is_valid_true_with_main_index_equal_to_zero(self):
        element = EmptyNode(main_index=0, sub_index=42)
        self.assertTrue(element.is_valid())

    def test_is_valid_false_with_sub_index_equal_to_zero(self):
        element = EmptyNode(main_index=42, sub_index=0)
        self.assertFalse(element.is_valid())

    def test_is_valid_true_with_main_index_greater_than_zero(self):
        element = EmptyNode(main_index=1, sub_index=42)
        self.assertTrue(element.is_valid())

    def test_is_valid_true_with_sub_index_greater_than_zero(self):
        element = EmptyNode(main_index=42, sub_index=1)
        self.assertTrue(element.is_valid())

    def test_is_valid_true_with_all_values_set(self):
        element = EmptyNode(
            main_index=1,
            sub_index=2,
            form='Form',
            lemma='Lemma',
            upos=UposTag.X,
            xpos='XPOS',
            feats={'foo': 'bar'},
            deps={'baz': 'qux'},
            misc='Misc'
        )
        self.assertTrue(element.is_valid())
