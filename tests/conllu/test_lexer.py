
import unittest
from typing import List
from ply.lex import Lexer, LexToken
from colonel.conllu.lexer import ConlluLexerBuilder, IllegalCharacterError


class TestConlluLexerBuilder(unittest.TestCase):

    @staticmethod
    def _tokenize(data: str) -> List[LexToken]:
        lexer = ConlluLexerBuilder.build()
        lexer.input(data)
        return list(lexer)

    def test_build_returns_a_lexer(self):
        self.assertIsInstance(ConlluLexerBuilder.build(), Lexer)

    def test_lexer_error_has_correct_line_and_column(self):
        data = '# Foo\n' \
               '# Bar\n' \
               '1\t_\t_\t_\tfoo bar\t_\t_\t_\t_\t_'  # illegal space

        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(3, err_context.exception.line_number)
        self.assertEqual(12, err_context.exception.column_number)

    def test_comment(self):
        data = '# A comment'
        tokens = self._tokenize(data)
        self.assertEqual(1, len(tokens))
        self.assertEqual('COMMENT', tokens[0].type)
        self.assertEqual('A comment', tokens[0].value)

    def test_comment_is_stripped(self):
        data = '#       A   comment       '
        tokens = self._tokenize(data)
        self.assertEqual(1, len(tokens))
        self.assertEqual('COMMENT', tokens[0].type)
        self.assertEqual('A   comment', tokens[0].value)

    def test_empty_comment(self):
        data = '#'
        tokens = self._tokenize(data)
        self.assertEqual(1, len(tokens))
        self.assertEqual('COMMENT', tokens[0].type)
        self.assertEqual('', tokens[0].value)

    def test_valid_all_underscores_except_id(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual(19, len(tokens))

    def test_valid_integer_id_with_one_digit(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('INTEGER_ID', tokens[0].type)
        self.assertEqual(1, tokens[0].value)

    def test_valid_integer_id_with_many_digits(self):
        data = '123\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('INTEGER_ID', tokens[0].type)
        self.assertEqual(123, tokens[0].value)

    def test_invalid_integer_id_equal_to_zero(self):
        data = '0\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(1, err_context.exception.column_number)

    def test_invalid_integer_id_with_leading_zero(self):
        data = '01\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(1, err_context.exception.column_number)

    def test_valid_range_id_with_one_digit(self):
        data = '1-2\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('RANGE_ID', tokens[0].type)
        self.assertEqual((1, 2), tokens[0].value)

    def test_valid_range_id_with_many_digits(self):
        data = '123-456\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('RANGE_ID', tokens[0].type)
        self.assertEqual((123, 456), tokens[0].value)

    def test_invalid_range_id_with_first_id_equal_to_zero(self):
        data = '0-1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(1, err_context.exception.column_number)

    def test_invalid_range_id_with_last_id_equal_to_zero(self):
        data = '1-0\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(2, err_context.exception.column_number)

    def test_invalid_range_id_with_first_id_with_leading_zero(self):
        data = '01-2\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(1, err_context.exception.column_number)

    def test_invalid_range_id_with_last_id_with_leading_zero(self):
        data = '1-02\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(2, err_context.exception.column_number)

    def test_valid_decimal_id_with_one_digit(self):
        data = '0.1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('DECIMAL_ID', tokens[0].type)
        self.assertEqual((0, 1), tokens[0].value)

    def test_valid_decimal_id_with_many_digit(self):
        data = '123.456\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('DECIMAL_ID', tokens[0].type)
        self.assertEqual((123, 456), tokens[0].value)

    def test_invalid_decimal_id_with_sub_id_equal_to_zero(self):
        data = '0.0\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(1, err_context.exception.column_number)

    def test_invalid_decimal_id_with_first_id_with_leading_zero(self):
        data = '01.1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(1, err_context.exception.column_number)

    def test_invalid_decimal_id_with_second_id_with_leading_zero(self):
        data = '0.01\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(1, err_context.exception.column_number)

    def test_invalid_empty_id_field(self):
        data = '\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(1, err_context.exception.column_number)

    def test_valid_simple_form(self):
        data = '1\tFoo!\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('FORM', tokens[2].type)
        self.assertEqual('Foo!', tokens[2].value)

    def test_valid_form_with_spaces(self):
        data = '1\tFoo Bar!\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('FORM', tokens[2].type)
        self.assertEqual('Foo Bar!', tokens[2].value)

    def test_valid_form_equal_to_underscore(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('FORM', tokens[2].type)
        self.assertEqual('_', tokens[2].value)

    def test_invalid_empty_form_field(self):
        data = '1\t\t_\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(3, err_context.exception.column_number)

    def test_valid_simple_lemma(self):
        data = '1\t_\tFoo!\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('LEMMA', tokens[4].type)
        self.assertEqual('Foo!', tokens[4].value)

    def test_valid_lemma_with_spaces(self):
        data = '1\t_\tFoo Bar!\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('LEMMA', tokens[4].type)
        self.assertEqual('Foo Bar!', tokens[4].value)

    def test_valid_lemma_equals_to_underscore(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('LEMMA', tokens[4].type)
        self.assertEqual('_', tokens[4].value)

    def test_invalid_empty_lemma_field(self):
        data = '1\t_\t\t_\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(5, err_context.exception.column_number)

    def test_valid_upos(self):
        data = '1\t_\t_\tVERB\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('UPOS', tokens[6].type)
        self.assertEqual('VERB', tokens[6].value)

    def test_valid_upos_equal_to_underscore(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('UPOS', tokens[6].type)
        self.assertIsNone(tokens[6].value)

    def test_invalid_upos(self):
        data = '1\t_\t_\tfoo\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(7, err_context.exception.column_number)

    def test_invalid_empty_upos_field(self):
        data = '1\t_\t_\t\t_\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(7, err_context.exception.column_number)

    def test_valid_xpos(self):
        data = '1\t_\t_\t_\tfoo\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('XPOS', tokens[8].type)
        self.assertEqual('foo', tokens[8].value)

    def test_valid_xpos_equal_to_underscore(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('XPOS', tokens[8].type)
        self.assertIsNone(tokens[8].value)

    def test_invalid_xpos_with_space(self):
        data = '1\t_\t_\t_\tfoo bar\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(12, err_context.exception.column_number)

    def test_invalid_empty_xpos_field(self):
        data = '1\t_\t_\t_\t\t_\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(9, err_context.exception.column_number)

    def test_valid_feats(self):
        data = '1\t_\t_\t_\t_\tAb=Cd|Ef[01]=G3|Hij=Klm,Nop\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('FEATS', tokens[10].type)

        expected = (
            ('Ab', ('Cd',)),
            ('Ef[01]', ('G3',)),
            ('Hij', ('Klm', 'Nop',))
        )
        self.assertEqual(expected, tokens[10].value)

    def test_valid_feats_equal_to_underscore(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('FEATS', tokens[10].type)
        self.assertIsNone(tokens[10].value)

    def test_invalid_feats(self):
        data = '1\t_\t_\t_\t_\tfoo\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(11, err_context.exception.column_number)

    def test_invalid_empty_feats_field(self):
        data = '1\t_\t_\t_\t_\t\t_\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(11, err_context.exception.column_number)

    def test_valid_head_with_one_digit(self):
        data = '1\t_\t_\t_\t_\t_\t0\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('HEAD', tokens[12].type)
        self.assertEqual(0, tokens[12].value)

    def test_valid_head_with_many_digits(self):
        data = '1\t_\t_\t_\t_\t_\t123\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('HEAD', tokens[12].type)
        self.assertEqual(123, tokens[12].value)

    def test_valid_head_equal_to_underscore(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('HEAD', tokens[12].type)
        self.assertIsNone(tokens[12].value)

    def test_invalid_head_with_leading_zero(self):
        data = '1\t_\t_\t_\t_\t_\t01\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(14, err_context.exception.column_number)

    def test_invalid_empty_head_field(self):
        data = '1\t_\t_\t_\t_\t_\t\t_\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(13, err_context.exception.column_number)

    def test_valid_deprel(self):
        data = '1\t_\t_\t_\t_\t_\t_\tFoo\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('DEPREL', tokens[14].type)
        self.assertEqual('Foo', tokens[14].value)

    def test_valid_deprel_equal_to_underscore(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('DEPREL', tokens[14].type)
        self.assertIsNone(tokens[14].value)

    def test_invalid_deprel_with_space(self):
        data = '1\t_\t_\t_\t_\t_\t_\tfoo bar\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(18, err_context.exception.column_number)

    def test_invalid_empty_deprel_field(self):
        data = '1\t_\t_\t_\t_\t_\t_\t\t_\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(15, err_context.exception.column_number)

    def test_valid_deps_with_one_digit(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t0:Foo|1:bar\t_'
        tokens = self._tokenize(data)
        self.assertEqual('DEPS', tokens[16].type)

        expected = ((0, 'Foo'), (1, 'bar'))
        self.assertEqual(expected, tokens[16].value)

    def test_valid_deps_with_many_digits(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t123:Foo|456:bar\t_'
        tokens = self._tokenize(data)
        self.assertEqual('DEPS', tokens[16].type)

        expected = ((123, 'Foo'), (456, 'bar'))
        self.assertEqual(expected, tokens[16].value)

    def test_valid_deps_equal_to_underscore(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('DEPS', tokens[16].type)
        self.assertIsNone(tokens[16].value)

    def test_invalid_deps(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\tfoo\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(17, err_context.exception.column_number)

    def test_invalid_deps_with_leading_zero(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t01:Foo\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(17, err_context.exception.column_number)

    def test_invalid_empty_deps_field(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t\t_'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(17, err_context.exception.column_number)

    def test_valid_misc(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\tFoo...Bar'
        tokens = self._tokenize(data)
        self.assertEqual('MISC', tokens[18].type)
        self.assertEqual('Foo...Bar', tokens[18].value)

    def test_valid_misc_equal_to_underscore(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t_'
        tokens = self._tokenize(data)
        self.assertEqual('MISC', tokens[18].type)
        self.assertIsNone(tokens[18].value)

    def test_invalid_misc_with_space(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\tfoo bar'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(22, err_context.exception.column_number)

    def test_invalid_empty_misc_field(self):
        data = '1\t_\t_\t_\t_\t_\t_\t_\t_\t\n'
        with self.assertRaises(IllegalCharacterError) as err_context:
            self._tokenize(data)

        self.assertEqual(1, err_context.exception.line_number)
        self.assertEqual(19, err_context.exception.column_number)

    def test_multiple_comments_and_word_lines(self):
        data = \
            '# Foo\n' \
            '# Bar\n' \
            '1\tF1\tL1\tADJ\tX1\tA=B|C=D\t2\tD1\t1:D1|2:D2\tM1\n' \
            '1.1\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
            '2\tF2\tL2\tADV\tX2\tE=F|G=H\t0\tD2\t2:D2\tM2\n' \
            '\n' \
            '# Baz\n' \
            '# Qux\n' \
            '1-2\t_\t_\t_\t_\t_\t_\t_\t_\t_\n' \
            '1\tF3\tL3\tINTJ\tX3\tU=V|W=X\t0\tD3\t_\tM3\n' \
            '2\tF4\tL4\tNOUN\tX4\tY=Z\t1\tD4\t_\tM4\n' \
            '\n'

        tokens = self._tokenize(data)

        self.assertEqual(130, len(tokens))

        self.assertEqual('COMMENT', tokens[0].type)
        self.assertEqual('Foo', tokens[0].value)
        self.assertEqual('NEWLINE', tokens[1].type)
        self.assertEqual('COMMENT', tokens[2].type)
        self.assertEqual('Bar', tokens[2].value)
        self.assertEqual('NEWLINE', tokens[3].type)

        self.assertEqual('INTEGER_ID', tokens[4].type)
        self.assertEqual(1, tokens[4].value)
        self.assertEqual('TAB', tokens[5].type)
        self.assertEqual('FORM', tokens[6].type)
        self.assertEqual('F1', tokens[6].value)
        self.assertEqual('TAB', tokens[7].type)
        self.assertEqual('LEMMA', tokens[8].type)
        self.assertEqual('L1', tokens[8].value)
        self.assertEqual('TAB', tokens[9].type)
        self.assertEqual('UPOS', tokens[10].type)
        self.assertEqual('ADJ', tokens[10].value)
        self.assertEqual('TAB', tokens[11].type)
        self.assertEqual('XPOS', tokens[12].type)
        self.assertEqual('X1', tokens[12].value)
        self.assertEqual('TAB', tokens[13].type)
        self.assertEqual('FEATS', tokens[14].type)
        self.assertEqual((('A', ('B',)), ('C', ('D',))), tokens[14].value)
        self.assertEqual('TAB', tokens[15].type)
        self.assertEqual('HEAD', tokens[16].type)
        self.assertEqual(2, tokens[16].value)
        self.assertEqual('TAB', tokens[17].type)
        self.assertEqual('DEPREL', tokens[18].type)
        self.assertEqual('D1', tokens[18].value)
        self.assertEqual('TAB', tokens[19].type)
        self.assertEqual('DEPS', tokens[20].type)
        self.assertEqual(((1, 'D1'), (2, 'D2')), tokens[20].value)
        self.assertEqual('TAB', tokens[21].type)
        self.assertEqual('MISC', tokens[22].type)
        self.assertEqual('M1', tokens[22].value)
        self.assertEqual('NEWLINE', tokens[23].type)

        self.assertEqual('DECIMAL_ID', tokens[24].type)
        self.assertEqual((1, 1), tokens[24].value)
        self.assertEqual('TAB', tokens[25].type)
        self.assertEqual('FORM', tokens[26].type)
        self.assertEqual('_', tokens[26].value)
        self.assertEqual('TAB', tokens[27].type)
        self.assertEqual('LEMMA', tokens[28].type)
        self.assertEqual('_', tokens[28].value)
        self.assertEqual('TAB', tokens[29].type)
        self.assertEqual('UPOS', tokens[30].type)
        self.assertIsNone(tokens[30].value)
        self.assertEqual('TAB', tokens[31].type)
        self.assertEqual('XPOS', tokens[32].type)
        self.assertIsNone(tokens[32].value)
        self.assertEqual('TAB', tokens[33].type)
        self.assertEqual('FEATS', tokens[34].type)
        self.assertIsNone(tokens[34].value)
        self.assertEqual('TAB', tokens[35].type)
        self.assertEqual('HEAD', tokens[36].type)
        self.assertIsNone(tokens[36].value)
        self.assertEqual('TAB', tokens[37].type)
        self.assertEqual('DEPREL', tokens[38].type)
        self.assertIsNone(tokens[38].value)
        self.assertEqual('TAB', tokens[39].type)
        self.assertEqual('DEPS', tokens[40].type)
        self.assertIsNone(tokens[40].value)
        self.assertEqual('TAB', tokens[41].type)
        self.assertEqual('MISC', tokens[42].type)
        self.assertIsNone(tokens[42].value)
        self.assertEqual('NEWLINE', tokens[43].type)

        self.assertEqual('INTEGER_ID', tokens[44].type)
        self.assertEqual(2, tokens[44].value)
        self.assertEqual('TAB', tokens[45].type)
        self.assertEqual('FORM', tokens[46].type)
        self.assertEqual('F2', tokens[46].value)
        self.assertEqual('TAB', tokens[47].type)
        self.assertEqual('LEMMA', tokens[48].type)
        self.assertEqual('L2', tokens[48].value)
        self.assertEqual('TAB', tokens[49].type)
        self.assertEqual('UPOS', tokens[50].type)
        self.assertEqual('ADV', tokens[50].value)
        self.assertEqual('TAB', tokens[51].type)
        self.assertEqual('XPOS', tokens[52].type)
        self.assertEqual('X2', tokens[52].value)
        self.assertEqual('TAB', tokens[53].type)
        self.assertEqual('FEATS', tokens[54].type)
        self.assertEqual((('E', ('F',)), ('G', ('H',))), tokens[54].value)
        self.assertEqual('TAB', tokens[55].type)
        self.assertEqual('HEAD', tokens[56].type)
        self.assertEqual(0, tokens[56].value)
        self.assertEqual('TAB', tokens[57].type)
        self.assertEqual('DEPREL', tokens[58].type)
        self.assertEqual('D2', tokens[58].value)
        self.assertEqual('TAB', tokens[59].type)
        self.assertEqual('DEPS', tokens[60].type)
        self.assertEqual(((2, 'D2'),), tokens[60].value)
        self.assertEqual('TAB', tokens[61].type)
        self.assertEqual('MISC', tokens[62].type)
        self.assertEqual('M2', tokens[62].value)
        self.assertEqual('NEWLINE', tokens[63].type)
        self.assertEqual('NEWLINE', tokens[64].type)

        self.assertEqual('COMMENT', tokens[65].type)
        self.assertEqual('Baz', tokens[65].value)
        self.assertEqual('NEWLINE', tokens[66].type)
        self.assertEqual('COMMENT', tokens[67].type)
        self.assertEqual('Qux', tokens[67].value)
        self.assertEqual('NEWLINE', tokens[68].type)

        self.assertEqual('RANGE_ID', tokens[69].type)
        self.assertEqual((1, 2), tokens[69].value)
        self.assertEqual('TAB', tokens[70].type)
        self.assertEqual('FORM', tokens[71].type)
        self.assertEqual('_', tokens[71].value)
        self.assertEqual('TAB', tokens[72].type)
        self.assertEqual('LEMMA', tokens[73].type)
        self.assertEqual('_', tokens[73].value)
        self.assertEqual('TAB', tokens[74].type)
        self.assertEqual('UPOS', tokens[75].type)
        self.assertIsNone(tokens[75].value)
        self.assertEqual('TAB', tokens[76].type)
        self.assertEqual('XPOS', tokens[77].type)
        self.assertIsNone(tokens[77].value)
        self.assertEqual('TAB', tokens[78].type)
        self.assertEqual('FEATS', tokens[79].type)
        self.assertIsNone(tokens[79].value)
        self.assertEqual('TAB', tokens[80].type)
        self.assertEqual('HEAD', tokens[81].type)
        self.assertIsNone(tokens[81].value)
        self.assertEqual('TAB', tokens[82].type)
        self.assertEqual('DEPREL', tokens[83].type)
        self.assertIsNone(tokens[83].value)
        self.assertEqual('TAB', tokens[84].type)
        self.assertEqual('DEPS', tokens[85].type)
        self.assertIsNone(tokens[85].value)
        self.assertEqual('TAB', tokens[86].type)
        self.assertEqual('MISC', tokens[87].type)
        self.assertIsNone(tokens[87].value)
        self.assertEqual('NEWLINE', tokens[88].type)

        self.assertEqual('INTEGER_ID', tokens[89].type)
        self.assertEqual(1, tokens[89].value)
        self.assertEqual('TAB', tokens[90].type)
        self.assertEqual('FORM', tokens[91].type)
        self.assertEqual('F3', tokens[91].value)
        self.assertEqual('TAB', tokens[92].type)
        self.assertEqual('LEMMA', tokens[93].type)
        self.assertEqual('L3', tokens[93].value)
        self.assertEqual('TAB', tokens[94].type)
        self.assertEqual('UPOS', tokens[95].type)
        self.assertEqual('INTJ', tokens[95].value)
        self.assertEqual('TAB', tokens[96].type)
        self.assertEqual('XPOS', tokens[97].type)
        self.assertEqual('X3', tokens[97].value)
        self.assertEqual('TAB', tokens[98].type)
        self.assertEqual('FEATS', tokens[99].type)
        self.assertEqual((('U', ('V',)), ('W', ('X',))), tokens[99].value)
        self.assertEqual('TAB', tokens[100].type)
        self.assertEqual('HEAD', tokens[101].type)
        self.assertEqual(0, tokens[101].value)
        self.assertEqual('TAB', tokens[102].type)
        self.assertEqual('DEPREL', tokens[103].type)
        self.assertEqual('D3', tokens[103].value)
        self.assertEqual('TAB', tokens[104].type)
        self.assertEqual('DEPS', tokens[105].type)
        self.assertIsNone(tokens[105].value)
        self.assertEqual('TAB', tokens[106].type)
        self.assertEqual('MISC', tokens[107].type)
        self.assertEqual('M3', tokens[107].value)
        self.assertEqual('NEWLINE', tokens[108].type)

        self.assertEqual('INTEGER_ID', tokens[109].type)
        self.assertEqual(2, tokens[109].value)
        self.assertEqual('TAB', tokens[110].type)
        self.assertEqual('FORM', tokens[111].type)
        self.assertEqual('F4', tokens[111].value)
        self.assertEqual('TAB', tokens[112].type)
        self.assertEqual('LEMMA', tokens[113].type)
        self.assertEqual('L4', tokens[113].value)
        self.assertEqual('TAB', tokens[114].type)
        self.assertEqual('UPOS', tokens[115].type)
        self.assertEqual('NOUN', tokens[115].value)
        self.assertEqual('TAB', tokens[116].type)
        self.assertEqual('XPOS', tokens[117].type)
        self.assertEqual('X4', tokens[117].value)
        self.assertEqual('TAB', tokens[118].type)
        self.assertEqual('FEATS', tokens[119].type)
        self.assertEqual((('Y', ('Z',)),), tokens[119].value)
        self.assertEqual('TAB', tokens[120].type)
        self.assertEqual('HEAD', tokens[121].type)
        self.assertEqual(1, tokens[121].value)
        self.assertEqual('TAB', tokens[122].type)
        self.assertEqual('DEPREL', tokens[123].type)
        self.assertEqual('D4', tokens[123].value)
        self.assertEqual('TAB', tokens[124].type)
        self.assertEqual('DEPS', tokens[125].type)
        self.assertIsNone(tokens[125].value)
        self.assertEqual('TAB', tokens[126].type)
        self.assertEqual('MISC', tokens[127].type)
        self.assertEqual('M4', tokens[127].value)
        self.assertEqual('NEWLINE', tokens[128].type)
        self.assertEqual('NEWLINE', tokens[129].type)
