from __future__ import annotations

from typing import Optional

from .token import Token
from ..contexts import ParagraphContext, ContextManager


class ParagraphEndToken(Token):
    def walk(self, ctx: ContextManager):

        if ctx.exist_goto(ParagraphContext):
            ctx.goto(ParagraphContext)
            ctx.pop()

    @staticmethod
    def parse(source: str) -> Optional[ParagraphEndToken]:
        text = source.lstrip().rstrip()

        if text == '':
            return ParagraphEndToken()
