from unittest import TestCase

from models import LexingState, TokenType
from lexer.lexer import Lexer


class LexerGeneralTests(TestCase):

    def test_add_token_no_rollback(self):
        lexer = Lexer('123')
        lexer.token_buffer = '12345'
        lexer.state = LexingState.LIT_STR
        lexer.offset = 4

        lexer.add_token(TokenType.OP_PLUS)

        self.assertEqual(1, len(lexer.tokens))
        self.assertEqual('', lexer.token_buffer)
        self.assertEqual(LexingState.START, lexer.state)
        self.assertEqual(lexer.offset, 4)

    def test_add_token_rollback(self):
        lexer = Lexer('123')
        lexer.offset = 4

        lexer.add_token(TokenType.OP_PLUS, rollback=True)

        self.assertEqual(lexer.offset, 3)

    def test_begin_tokenizing_no_new_state(self):
        lexer = Lexer('123')
        lexer.line_number = 5
        lexer.state = LexingState.LIT_STR

        lexer.begin_tokenizing()

        self.assertEqual(LexingState.LIT_STR, lexer.state)
        self.assertEqual('1', lexer.token_buffer)
        self.assertEqual(5, lexer.token_start_line_number)

    def test_begin_tokenizing_new_state(self):
        lexer = Lexer('123')

        lexer.begin_tokenizing(LexingState.LIT_STR)

        self.assertEqual(LexingState.LIT_STR, lexer.state)
