from __future__ import annotations

from typing import Optional

from .token import Token
from ..contexts import ContextManager
from ..contexts import PageContext, PageHeadingTextContext, \
    HeadingTextContext, \
    SubHeadingTextContext


class HeaderToken(Token):
    def __init__(self, level: int, text: str):
        self.level = level
        self.text = text

    def walk(self, ctx: ContextManager):
        if self.level == 1:
            current_ctx = ctx.current()
            if current_ctx is None or \
                    type(current_ctx) is not PageContext or \
                    len(current_ctx.children) > 0:
                current_ctx = ctx.create_branch(PageContext, title=self.text)

            current_ctx.title = self.text

            header_context = ctx.push_create(PageHeadingTextContext)
            header_context.text = self.text
        elif self.level == 2:
            ctx.push_create(HeadingTextContext, text=self.text)
        else:
            ctx.push_create(SubHeadingTextContext, text=self.text)
        return

    @staticmethod
    def parse(source: str) -> Optional[HeaderToken]:
        levels = ['# ', '## ', '### ']

        for i, pattern in enumerate(levels):
            level = i + 1
            if source.startswith(pattern) and source != pattern:
                text = source[len(pattern):]
                text = text.lstrip().rstrip()
                return HeaderToken(level, text)
