from __future__ import annotations

import re
from typing import Optional

from .token import Token
from ..contexts import ContextManager, EnumerateHeadingContext


class EnumerateToken(Token):
    def __init__(self, level: int, text: str):
        self.level = level
        self.text = text

    def walk(self, ctx: ContextManager):
        ctx.push_create(EnumerateHeadingContext, level=self.level, text=self.text)

    @staticmethod
    def parse(source: str) -> Optional[EnumerateToken]:
        source = source.lstrip().rstrip()
        pattern = r'^[0-9]*[.][ ]'

        match = re.match(pattern, source)
        if match:
            reg = match.regs[0]

            level = int(source[:reg[1] - 2])
            text = source[reg[1]:].lstrip()

            return EnumerateToken(level, text)
