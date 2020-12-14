from __future__ import annotations

from typing import Optional

from .token import Token
from ..contexts import ParagraphContext, ContextManager, TableBlockContext


class FileToken(Token):
    def __init__(self, base_file_url: str):
        self.base_file_url = base_file_url

    def walk(self, ctx: ContextManager):
        from ..contexts import FileContext
        ctx.create_branch(FileContext, base_file_url=self.base_file_url)


class ParagraphEndToken(Token):
    def walk(self, ctx: ContextManager):

        if ctx.exist_goto(ParagraphContext):
            ctx.goto(ParagraphContext)
            ctx.pop()

        if ctx.exist_goto(TableBlockContext):
            ctx.goto(TableBlockContext)
            ctx.pop()

    @staticmethod
    def parse(source: str) -> Optional[ParagraphEndToken]:
        text = source.lstrip().rstrip()

        if text == '':
            return ParagraphEndToken()
