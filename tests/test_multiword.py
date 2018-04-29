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
from colonel.multiword import Multiword


class TestMultiword(unittest.TestCase):

    def test_init_first_index(self):
        element = Multiword(first_index=42)
        self.assertEqual(42, element.first_index)

    def test_init_last_index(self):
        element = Multiword(last_index=42)
        self.assertEqual(42, element.last_index)

    def test_init_form(self):
        element = Multiword(form='Foo')
        self.assertEqual('Foo', element.form)

    def test_init_misc(self):
        element = Multiword(misc='Foo')
        self.assertEqual('Foo', element.misc)

    def test_is_valid_false_with_no_values_set(self):
        element = Multiword()
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_first_index_is_not_set(self):
        element = Multiword(last_index=42)
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_last_index_is_not_set(self):
        element = Multiword(first_index=42)
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_first_index_less_than_zero(self):
        element = Multiword(first_index=-1, last_index=42)
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_first_index_equal_to_zero(self):
        element = Multiword(first_index=0, last_index=42)
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_last_index_lower_to_first_index(self):
        element = Multiword(first_index=42, last_index=5)
        self.assertFalse(element.is_valid())

    def test_is_valid_false_with_last_index_equal_to_first_index(self):
        element = Multiword(first_index=42, last_index=42)
        self.assertFalse(element.is_valid())

    def test_is_valid_true_with_first_index_greater_than_zero(self):
        element = Multiword(first_index=1, last_index=42)
        self.assertTrue(element.is_valid())

    def test_is_valid_true_with_all_values_set(self):
        element = Multiword(
            first_index=1,
            last_index=2,
            form='Form',
            misc='Misc'
        )
        self.assertTrue(element.is_valid())

    def test_to_conllu_of_invalid_sentence_with_no_attributes(self):
        multiword = Multiword()
        self.assertEqual(
            'None-None\t_\t_\t_\t_\t_\t_\t_\t_\t_', multiword.to_conllu())

    def test_to_conllu_of_sentence_with_all_attributes(self):
        multiword = Multiword(
            first_index=1,
            last_index=2,
            form='Form',
            misc='Misc')

        self.assertEqual(
            '1-2\tForm\t_\t_\t_\t_\t_\t_\t_\tMisc',
            multiword.to_conllu())
