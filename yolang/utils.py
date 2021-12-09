from typing import Any, Iterable, Iterator, TypeVar
from contextlib import suppress

from .tokenizer import Token, TokenType

T = TypeVar('T', bound=Any)


class CacheIterator(Iterator[T]):
    def __init__(
        self,
        it: Iterable[T],
    ) -> None:
        self.it = iter(it)

        self.cache: list[T] = []
        self.index = 0

    def __next__(self) -> T:
        if self.index != 0:
            self.index -= 1
            return self.cache[self.index]

        value = next(self.it)
        self.cache.append(value)

        return value

    def __iter__(self) -> Iterator[T]:
        return self

    def back(self, n: int = 1) -> None:
        if n > len(self.cache):
            raise IndexError("Not enough elements in cache")

        self.index += n


class TokensIterator(CacheIterator[Token]):
    @property
    def _actual(self) -> Token:
        with suppress(IndexError):
            self.back()

        return next(self)

    def eat(
        self,
        kind: TokenType,
    ) -> Token | None:
        if self.check(kind):
            return self._actual

    def check(
        self,
        kind: TokenType,
    ) -> bool:
        return self._actual.kind is kind

    def lookup(self) -> Token:
        value = next(self)
        self.back()

        return value
