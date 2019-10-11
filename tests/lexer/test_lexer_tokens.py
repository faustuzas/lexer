from unittest import TestCase

from models import TokenError

from models import TokenType
from lexer.lexer import Lexer


class LexerTokensTests(TestCase):

    def test_op_plus(self):
        lexer = Lexer('+')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_PLUS, lexer.tokens[0].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[1].type)

    def test_op_plus_2(self):
        lexer = Lexer('+ + +')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_PLUS, lexer.tokens[0].type)
        self.assertEqual(TokenType.OP_PLUS, lexer.tokens[1].type)
        self.assertEqual(TokenType.OP_PLUS, lexer.tokens[2].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[3].type)

    def test_op_minus(self):
        lexer = Lexer('-')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[0].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[1].type)

    def test_op_minus_2(self):
        lexer = Lexer('---')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[0].type)
        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[1].type)
        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[2].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[3].type)

    def test_op_minus_3(self):
        lexer = Lexer('- - -')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[0].type)
        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[1].type)
        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[2].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[3].type)

    def test_to_stdout(self):
        lexer = Lexer('-->')

        lexer.lex_all()

        self.assertEqual(TokenType.KW_TO_STDOUT, lexer.tokens[0].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[1].type)

    def test_to_stdout_2(self):
        lexer = Lexer('--->---->-->-')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[0].type)
        self.assertEqual(TokenType.KW_TO_STDOUT, lexer.tokens[1].type)
        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[2].type)
        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[3].type)
        self.assertEqual(TokenType.KW_TO_STDOUT, lexer.tokens[4].type)
        self.assertEqual(TokenType.KW_TO_STDOUT, lexer.tokens[5].type)
        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[6].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[7].type)

    def test_div(self):
        lexer = Lexer('/ /')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_DIV, lexer.tokens[0].type)
        self.assertEqual(TokenType.OP_DIV, lexer.tokens[1].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[2].type)

    def test_single_comment(self):
        lexer = Lexer('+ // test + test - test')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_PLUS, lexer.tokens[0].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[1].type)

    def test_single_comment_2(self):
        lexer = Lexer('\n / \n + // test + test - test \n - \n')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_DIV, lexer.tokens[0].type)
        self.assertEqual(2, lexer.tokens[0].line_number)
        self.assertEqual(TokenType.OP_PLUS, lexer.tokens[1].type)
        self.assertEqual(3, lexer.tokens[1].line_number)
        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[2].type)
        self.assertEqual(4, lexer.tokens[2].line_number)
        self.assertEqual(TokenType.EOF, lexer.tokens[3].type)

    def test_multi_comment_start(self):
        lexer = Lexer('\n / \n + /* test \n + test - \n * test */ \n - \n')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_DIV, lexer.tokens[0].type)
        self.assertEqual(2, lexer.tokens[0].line_number)
        self.assertEqual(TokenType.OP_PLUS, lexer.tokens[1].type)
        self.assertEqual(3, lexer.tokens[1].line_number)
        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[2].type)
        self.assertEqual(6, lexer.tokens[2].line_number)
        self.assertEqual(TokenType.EOF, lexer.tokens[3].type)

    def test_op_mul(self):
        lexer = Lexer('* /* + */ *')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_MUL, lexer.tokens[0].type)
        self.assertEqual(TokenType.OP_MUL, lexer.tokens[1].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[2].type)

    def test_op_pov(self):
        lexer = Lexer('^')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_POV, lexer.tokens[0].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[1].type)

    def test_op_mod(self):
        lexer = Lexer('%')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_MOD, lexer.tokens[0].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[1].type)

    def test_op_ne_and_op_not(self):
        lexer = Lexer('!=!!!=!')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_NE, lexer.tokens[0].type)
        self.assertEqual(TokenType.OP_NOT, lexer.tokens[1].type)
        self.assertEqual(TokenType.OP_NOT, lexer.tokens[2].type)
        self.assertEqual(TokenType.OP_NE, lexer.tokens[3].type)
        self.assertEqual(TokenType.OP_NOT, lexer.tokens[4].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[5].type)

    def test_op_eq_and_op_assign(self):
        lexer = Lexer('=====')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_EQ, lexer.tokens[0].type)
        self.assertEqual(TokenType.OP_EQ, lexer.tokens[1].type)
        self.assertEqual(TokenType.OP_ASSIGN, lexer.tokens[2].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[3].type)

    def test_op_eq_and_op_assign_2(self):
        lexer = Lexer('!= != == = ! != != => == =>')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_NE, lexer.tokens[0].type)
        self.assertEqual(TokenType.OP_NE, lexer.tokens[1].type)
        self.assertEqual(TokenType.OP_EQ, lexer.tokens[2].type)
        self.assertEqual(TokenType.OP_ASSIGN, lexer.tokens[3].type)
        self.assertEqual(TokenType.OP_NOT, lexer.tokens[4].type)
        self.assertEqual(TokenType.OP_NE, lexer.tokens[5].type)
        self.assertEqual(TokenType.OP_NE, lexer.tokens[6].type)
        self.assertEqual(TokenType.KW_FAT_ARROW, lexer.tokens[7].type)
        self.assertEqual(TokenType.OP_EQ, lexer.tokens[8].type)
        self.assertEqual(TokenType.KW_FAT_ARROW, lexer.tokens[9].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[10].type)

    def test_bunch_of_single_chars(self):
        lexer = Lexer(',:;({[]})')

        lexer.lex_all()

        self.assertEqual(TokenType.C_COMMA, lexer.tokens[0].type)
        self.assertEqual(TokenType.C_COLON, lexer.tokens[1].type)
        self.assertEqual(TokenType.C_SEMI, lexer.tokens[2].type)
        self.assertEqual(TokenType.C_ROUND_L, lexer.tokens[3].type)
        self.assertEqual(TokenType.C_CURLY_L, lexer.tokens[4].type)
        self.assertEqual(TokenType.C_SQUARE_L, lexer.tokens[5].type)
        self.assertEqual(TokenType.C_SQUARE_R, lexer.tokens[6].type)
        self.assertEqual(TokenType.C_CURLY_R, lexer.tokens[7].type)
        self.assertEqual(TokenType.C_ROUND_R, lexer.tokens[8].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[9].type)

    def test_op_and(self):
        lexer = Lexer('&&')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_AND, lexer.tokens[0].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[1].type)

    def test_op_and_error(self):
        lexer = Lexer('&')

        self.assertRaises(TokenError, lexer.lex_all)

    def test_op_or(self):
        lexer = Lexer('||')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_OR, lexer.tokens[0].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[1].type)

    def test_op_or_error(self):
        lexer = Lexer('|')

        self.assertRaises(TokenError, lexer.lex_all)

    def test_op_lt(self):
        lexer = Lexer('<')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_LT, lexer.tokens[0].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[1].type)

    def test_op_le(self):
        lexer = Lexer('<=')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_LE, lexer.tokens[0].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[1].type)

    def test_kw_from_stdin(self):
        lexer = Lexer('<-- <- <')

        lexer.lex_all()

        self.assertEqual(TokenType.KW_FROM_STDIN, lexer.tokens[0].type)
        self.assertEqual(TokenType.OP_LT, lexer.tokens[1].type)
        self.assertEqual(TokenType.OP_MINUS, lexer.tokens[2].type)
        self.assertEqual(TokenType.OP_LT, lexer.tokens[3].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[4].type)

    def test_op_access(self):
        lexer = Lexer('..')

        lexer.lex_all()

        self.assertEqual(TokenType.OP_ACCESS, lexer.tokens[0].type)
        self.assertEqual(TokenType.OP_ACCESS, lexer.tokens[1].type)
        self.assertEqual(TokenType.EOF, lexer.tokens[2].type)
