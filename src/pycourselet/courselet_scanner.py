import logging
import os
from typing import Generator, List

from jinja2 import FileSystemLoader, Environment

from .contexts import ContextManager, PageContext
from .tokens import *


class CourseletScanner:
    def scan_directory(self, dir_path: str) -> ContextManager:
        def key_function(key):
            if (i := key.find('_')) >= 0:
                try:
                    key = float(key[:i])
                except Exception as ex:
                    logging.exception(ex)
            return key

        file_loader = FileSystemLoader(os.path.abspath(dir_path))
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True

        ctx = ContextManager()

        list_dir = os.listdir(dir_path)
        sorted_list_dir = sorted(list_dir, key=key_function)
        for item_name in sorted_list_dir:
            item_path = os.path.join(dir_path, item_name)
            if os.path.isfile(item_path):
                title = item_name
                if (i := title.find('_')) >= 0:
                    title = title[i + 1:]
                if (i := title.rfind('.')) >= 0:
                    title = title[:i]
                ctx.create_branch(PageContext, title=title)

                template = env.get_template(item_name)
                output = template.render()
                self.scan(output, ctx)

        return ctx

    def scan(self, source: str, ctx: ContextManager = ContextManager()) \
            -> ContextManager:
        tokens: List[Token] = list()
        for line in source.splitlines():
            for line_token in self._parse_line(line):
                tokens.append(line_token)

        self._walk_tokens(tokens, ctx)

        return ctx

    def _parse_line(self, line: str) -> Generator[Token, None, None]:
        # Line Tokens
        if header_token := HeaderToken.parse(line):
            yield header_token

    def _walk_tokens(self, tokens: List[Token], ctx: ContextManager):

        for token in tokens:
            token.walk(ctx)

        return ctx
