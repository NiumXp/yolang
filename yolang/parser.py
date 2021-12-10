from .utils import TokensIterator


class Parser:
    def __init__(self, tokens: TokensIterator):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> ...:
        ...


def parse(tokens: TokensIterator) -> ...:
    ...
