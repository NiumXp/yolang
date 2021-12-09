from enum import IntEnum
from typing import Any, Iterable
from dataclasses import dataclass

RAW_SYMBOLS = "()<>+-*/[]=.,{}:"
WHITESPACES = " \t\n"
DOUBLE_RAW_SYMBOLS = {
    '>': '=',
    '<': '=',
    '=': '='
}


class TokenType(IntEnum):
    SYMBOL      = 0
    IDENTIFIER  = 1
    LITERAL     = 2
    WHITESPACE  = 3
    EOF         = 4


@dataclass
class Token:
    kind: TokenType
    value: Any
    position: tuple[int, int]


class Tokenizer:
    def __init__(self, source: str) -> None:
        self.source = source

        self._i = 0
        self._l = 0
        self._c = 0

    @property
    def eof(self) -> bool:
        return self._i >= len(self.source)

    @property
    def position(self) -> tuple[int, int]:
        return (self._l, self._c)

    def _symbol(self, char: str) -> Token:
        position = self.position

        self._c += 1
        self._i += 1

        double = DOUBLE_RAW_SYMBOLS.get(char)
        if (
            double
            and self.source[self._i] == double
        ):
            self._i += 1
            self._c += 1

            return Token(TokenType.SYMBOL, char+double, position)

        return Token(TokenType.SYMBOL, char, position)

    def _digit(self) -> Token:
        position = self.position

        value = ''

        while not self.eof and self.source[self._i].isdigit():
            value += self.source[self._i]

            self._i += 1
            self._c += 1

        return Token(TokenType.LITERAL, int(value), position)

    def _identifier(self) -> Token:
        value = ''

        while self.source[self._i].isalnum():
            value += self.source[self._i]
            self._i += 1
            self._c += 1

        return Token(TokenType.IDENTIFIER, value, self.position)

    def _string(self) -> Token:
        value = ''
        quote = self.source[self._i]

        self._i += 1
        self._c += 1

        while self.source[self._i] != quote:
            value += self.source[self._i]
            self._i += 1
            self._c += 1

        self._i += 1
        self._c += 1

        return Token(TokenType.LITERAL, value, self.position)

    def __next__(self) -> Token:
        if self.eof:
            return Token(TokenType.EOF, None, self.position)

        char = self.source[self._i]

        while char in WHITESPACES:
            if char == "\n":
                self._l += 1
                self._c = 0

            self._i += 1

            if self.eof:
                return next(self)

            char = self.source[self._i]

        if char in RAW_SYMBOLS:
            return self._symbol(char)

        if char.isalpha():
            return self._identifier()

        if char.isdigit():
            return self._digit()

        if char in "\"'":
            return self._string()

        raise SyntaxError(f"Unexpected character {char!r} at {self.position}")

    def __iter__(self):
        while not self.eof:
            yield next(self)

        yield next(self)  # EOF


def tokenize(code: str) -> Iterable[Token]:
    yield from Tokenizer(code)
