from __future__ import annotations

import re
from typing import Optional, List

from .token import Token
from ..contexts import ContextManager


class TableRowToken(Token):
    def __init__(self, row: List[List[Token]], no_print: bool = False):
        self.no_print = no_print
        self.row = row

    def walk(self, ctx: ContextManager):
        from ..contexts import TableBlockContext, TableRowBreakContext, \
            TableColumnBreakContext

        if self.no_print:
            return

        if ctx.exist_goto(TableBlockContext):
            ctx.push_create(TableRowBreakContext)
        else:
            ctx.push_create(TableBlockContext)

        for i, item in enumerate(self.row):
            for token in item:
                token.walk(ctx)
            if i == len(self.row) - 1:
                continue
            ctx.push_create(TableColumnBreakContext)

    @staticmethod
    def parse(source: str) -> Optional[TableRowToken]:
        source = source.lstrip().rstrip()

        if not (source.startswith('|') and source.endswith('|')):
            return

        items = [row.replace('\\|', '|').lstrip().rstrip()
                 for row in re.split(r'(?<!\\)\|', source)[1:-1]]

        no_print = True

        for item in items:
            if item.count('-') != len(item):
                no_print = False
                break

        if not no_print:
            from .text_tokens import TextToken
            row_tokens = list()
            for item in items:
                item_tokens = list()
                for item_token in TextToken.parse(item):
                    item_tokens.append(item_token)
                row_tokens.append(item_tokens)

            items = row_tokens

        return TableRowToken(items, no_print)
