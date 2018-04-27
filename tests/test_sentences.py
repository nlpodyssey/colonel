
import unittest
from typing import Generator
from colonel.sentence import Sentence
from colonel.word import Word
from colonel.emptynode import EmptyNode
from colonel.multiword import Multiword


class TestSentence(unittest.TestCase):

    def test_init_with_some_elements(self):
        elements = [Word(index=1), Word(index=2)]

        sentence = Sentence(elements)
        self.assertIs(sentence.elements, elements)

    def test_init_with_empty_elements(self):
        elements = []

        sentence = Sentence(elements)
        self.assertIs(sentence.elements, elements)

    def test_init_without_elements(self):
        sentence = Sentence()
        self.assertEqual([], sentence.elements)

    def test_init_with_some_comments(self):
        comments = ['Foo', 'Bar']

        sentence = Sentence(None, comments)
        self.assertIs(sentence.comments, comments)

    def test_init_with_empty_comments(self):
        comments = []

        sentence = Sentence(None, comments)
        self.assertIs(sentence.comments, comments)

    def test_init_without_comments(self):
        sentence = Sentence()
        self.assertEqual([], sentence.comments)

    def test_words_on_sentence_wit_mixed_element(self):
        expected = [
            Word(index=1),
            Word(index=2),
            Word(index=3),
            Word(index=4)
        ]

        sentence = Sentence([
            Multiword(first_index=1, last_index=2),
            expected[0],  # 1
            expected[1],  # 2
            EmptyNode(main_index=2, sub_index=1),
            EmptyNode(main_index=2, sub_index=2),
            Multiword(first_index=3, last_index=4),
            expected[2],  # 3
            expected[3],  # 4
        ])

        result = sentence.words()
        self.assertIsInstance(result, Generator)
        self.assertEqual(expected, list(result))

    def test_words_on_sentence_without_word_elements(self):
        sentence = Sentence([
            EmptyNode(main_index=0, sub_index=1),
            Multiword(first_index=1, last_index=2),
        ])

        result = sentence.words()
        self.assertIsInstance(result, Generator)
        self.assertEqual([], list(result))

    def test_words_on_empty_sentence(self):
        sentence = Sentence()

        result = sentence.words()
        self.assertIsInstance(result, Generator)
        self.assertEqual([], list(result))

    def test_raw_tokens_on_sentence_wit_mixed_element(self):
        expected = [
            Multiword(first_index=1, last_index=2),
            Word(index=3),
            Multiword(first_index=4, last_index=6),
            Word(index=7)
        ]

        sentence = Sentence([
            expected[0],  # 1-2
            Word(index=1),
            Word(index=2),
            expected[1],  # 3
            EmptyNode(main_index=3, sub_index=1),
            EmptyNode(main_index=3, sub_index=2),
            expected[2],  # 4-6
            Word(index=4),
            EmptyNode(main_index=4, sub_index=1),
            EmptyNode(main_index=4, sub_index=2),
            Word(index=5),
            Word(index=6),
            expected[3]  # 7
        ])

        result = sentence.raw_tokens()
        self.assertIsInstance(result, Generator)
        self.assertEqual(expected, list(result))

    def test_raw_tokens_on_sentence_without_word_and_multiwords(self):
        sentence = Sentence([
            EmptyNode(main_index=0, sub_index=1),
        ])

        result = sentence.raw_tokens()
        self.assertIsInstance(result, Generator)
        self.assertEqual([], list(result))

    def test_raw_tokens_on_empty_sentence(self):
        sentence = Sentence()

        result = sentence.raw_tokens()
        self.assertIsInstance(result, Generator)
        self.assertEqual([], list(result))

    def test_is_valid_false_on_empty_sentence(self):
        sentence = Sentence()
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_on_sentence_without_word_elements(self):
        sentence = Sentence([
            EmptyNode(main_index=0, sub_index=1),
            Multiword(first_index=1, last_index=2)
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_on_sentence_with_invalid_elements(self):
        sentence = Sentence([
            Multiword(first_index=1, last_index=1),  # invalid first == last
            Word(index=1),
            Word(index=2),
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_if_first_element_is_word_with_index_not_1(self):
        sentence = Sentence([
            Word(index=2)
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_true_if_first_element_is_word_with_index_1(self):
        sentence = Sentence([
            Word(index=1)
        ])
        self.assertTrue(sentence.is_valid())

    def test_is_valid_false_if_first_element_is_multiword_with_index_not_1(
            self
    ):
        sentence = Sentence([
            Multiword(first_index=2, last_index=5)
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_true_if_first_element_is_multiword_with_index_1(self):
        sentence = Sentence([
            Multiword(first_index=1, last_index=2),
            # words also included to prevent other validations to fail
            Word(index=1),
            Word(index=2),
        ])
        self.assertTrue(sentence.is_valid())

    def test_is_valid_false_if_first_element_is_emptynode_with_index_not_0(
            self
    ):
        sentence = Sentence([
            EmptyNode(main_index=1, sub_index=1)
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_true_if_first_element_is_emptynode_with_index_0(self):
        sentence = Sentence([
            EmptyNode(main_index=0, sub_index=1),
            # first word also included to prevent other validations to fail
            Word(index=1)
        ])
        self.assertTrue(sentence.is_valid())

    def test_is_valid_false_if_consecutive_multiwords_overlap(self):
        sentence = Sentence([
            Multiword(first_index=1, last_index=2),
            Multiword(first_index=1, last_index=2),
            Word(index=1),
            Word(index=2)
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_if_nonconsecutive_multiwords_overlap(self):
        sentence = Sentence([
            Multiword(first_index=1, last_index=2),
            Word(index=1),
            Multiword(first_index=2, last_index=3),
            Word(index=2),
            Word(index=3)
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_if_a_word_index_is_skipped(self):
        sentence = Sentence([
            Word(index=1),
            Word(index=2),
            # index 3 missing
            Word(index=4),
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_true_with_two_consecutive_word_indexes(self):
        sentence = Sentence([
            Word(index=1),
            Word(index=2),
        ])
        self.assertTrue(sentence.is_valid())

    def test_is_valid_false_if_multiword_index_is_skipped(self):
        sentence = Sentence([
            Word(index=1),
            # index 2 missing
            Multiword(first_index=3, last_index=4),
            Word(index=3),
            Word(index=4),
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_if_multiword_last_index_is_too_big(self):
        sentence = Sentence([
            Word(index=1),
            Multiword(first_index=2, last_index=4),  # there is no word w/ ID 4
            Word(index=2),
            Word(index=3),
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_true_if_multiword_index_range_is_within_sentence_bounds(
            self
    ):
        sentence = Sentence([
            Word(index=1),
            Multiword(first_index=2, last_index=3),
            Word(index=2),
            Word(index=3)
        ])
        self.assertTrue(sentence.is_valid())

    def test_is_valid_false_if_two_emptynodes_has_the_same_sub_index(self):
        sentence = Sentence([
            EmptyNode(main_index=0, sub_index=1),
            EmptyNode(main_index=0, sub_index=1),
            Word(index=1),
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_if_an_emptynode_sub_index_is_skipped(self):
        sentence = Sentence([
            EmptyNode(main_index=0, sub_index=1),
            # sub_index 2 missing
            EmptyNode(main_index=0, sub_index=3),
            Word(index=1),
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_if_an_emptynode_main_index_has_no_word_index(self):
        sentence = Sentence([
            Word(index=1),
            # there is no word with index 2
            EmptyNode(main_index=2, sub_index=1),
            EmptyNode(main_index=2, sub_index=2)
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_if_consecutive_emptynodes_have_different_main_id(
            self
    ):
        sentence = Sentence([
            Word(index=1),
            EmptyNode(main_index=1, sub_index=1),
            # word with index 2 missing
            EmptyNode(main_index=2, sub_index=2)
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_true_if_emptynodes_indexes_are_valid(self):
        sentence = Sentence([
            EmptyNode(main_index=0, sub_index=1),
            EmptyNode(main_index=0, sub_index=2),
            Word(index=1),
            Word(index=2),
            EmptyNode(main_index=2, sub_index=1),
            EmptyNode(main_index=2, sub_index=2),
        ])
        self.assertTrue(sentence.is_valid())

    def test_is_valid_false_if_multiwords_are_placed_incorrectly(self):
        sentence = Sentence([
            Multiword(first_index=1, last_index=2),
            Multiword(first_index=3, last_index=4),  # should be before word 3
            Word(index=1),
            Word(index=2),
            Word(index=3),
            Word(index=4)
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_if_a_word_has_head_less_than_zero(self):
        sentence = Sentence([
            Word(index=1, head=-1),
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_false_if_a_word_has_head_beyond_last_word_index(self):
        sentence = Sentence([
            Word(index=1, head=2),  # there is no word with index 2
        ])
        self.assertFalse(sentence.is_valid())

    def test_is_valid_true_if_a_word_has_head_zero(self):
        sentence = Sentence([
            Word(index=1, head=0)
        ])
        self.assertTrue(sentence.is_valid())

    def test_is_valid_true_if_a_word_has_head_equals_to_index(self):
        sentence = Sentence([
            Word(index=1, head=1)
        ])
        self.assertTrue(sentence.is_valid())

    def test_is_valid_true_with_word_heads_within_sentence_bounds(self):
        sentence = Sentence([
            Word(index=1, head=2),
            Word(index=2, head=0),
        ])
        self.assertTrue(sentence.is_valid())
