import pytest

from yolang.tokenizer import tokenize, Token, TokenType
from yolang.utils import (
    CacheIterator,
    TokensIterator,
)

class TestCacheIterator:
    def test_next(self):
        it = range(10)
        it = CacheIterator(it)

        for index, number in enumerate(it):
            assert index == number

    def test_back(self):
        it = CacheIterator((1, 2, 3))

        with pytest.raises(IndexError):
            it.back()  # No cache

        next(it)  # 1
        next(it)  # 2

        it.back()

        assert next(it) == 1


class TestTokensIterator:
    def test_consume(self):
        it = tokenize("2+8")
        it = TokensIterator(it)

        assert next(it) == Token(TokenType.LITERAL, 2, (0, 0))
        assert next(it) == Token(TokenType.SYMBOL, '+', (0, 1))
        assert next(it) == Token(TokenType.LITERAL, 8, (0, 2))
        assert next(it) == Token(TokenType.EOF, None, (0, 3))

        with pytest.raises(StopIteration):
            next(it)
