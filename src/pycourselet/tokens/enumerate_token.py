from __future__ import annotations

import re
from typing import Optional, Tuple

from .token import Token
from ..contexts import ContextManager, EnumerateHeadingContext


class EnumerateToken(Token):
    def __init__(self, level: int):
        self.level = level

    def walk(self, ctx: ContextManager):
        ctx.push_create(EnumerateHeadingContext, level=self.level)

    @staticmethod
    def parse(source: str) -> Optional[Tuple[EnumerateToken, str]]:
        source = source.lstrip().rstrip()
        pattern = r'^[0-9]*[.][ ]'

        match = re.match(pattern, source)
        if match:
            reg = match.regs[0]

            level = int(source[:reg[1] - 2])
            text = source[reg[1]:].lstrip()

            return EnumerateToken(level), text
