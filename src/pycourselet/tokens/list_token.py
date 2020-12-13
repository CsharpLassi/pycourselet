from __future__ import annotations

from typing import Optional

from .token import Token
from ..contexts import ContextManager, ListHeadingContext


class ListToken(Token):
    def __init__(self, level: int, text: str):
        self.level = level
        self.text = text

    def walk(self, ctx: ContextManager):
        ctx.push_create(ListHeadingContext, text=self.text)

    @staticmethod
    def parse(source: str) -> Optional[ListToken]:
        source = source.lstrip().rstrip()
        levels = ['- ']

        for i, pattern in enumerate(levels):
            level = i + 1
            if source.startswith(pattern) and source != pattern:
                text = source[len(pattern):]
                text = text.lstrip().rstrip()
                return ListToken(level, text)
