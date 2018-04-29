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
from colonel.base_sentence_element import BaseSentenceElement


class TestBaseSentenceElement(unittest.TestCase):

    def test_init_form(self):
        element = BaseSentenceElement(form='Foo')
        self.assertEqual('Foo', element.form)

    def test_init_misc(self):
        element = BaseSentenceElement(misc='Foo')
        self.assertEqual('Foo', element.misc)

    def test_is_valid_true_with_no_values_set(self):
        element = BaseSentenceElement()
        self.assertTrue(element.is_valid())

    def test_is_valid_true_with_all_values_set(self):
        element = BaseSentenceElement(form='Foo', misc='Bar')
        self.assertTrue(element.is_valid())

    def to_conllu_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            BaseSentenceElement().to_conllu()
