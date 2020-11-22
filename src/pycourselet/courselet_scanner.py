import logging
import os
from typing import Generator, List

from jinja2 import FileSystemLoader, Environment

from .contexts import ContextManager, PageContext, FileContext
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
            item_path = os.path.abspath(item_path)

            ctx.push_create(FileContext, base_file_url=item_path)

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
            return

        # Picture Tokens
        if image_token := ImageToken.parse(line):
            yield image_token
            return

        # List Token
        if list_token := ListToken.parse(line):
            yield list_token
            return

        # Control Tokens
        if paragraph_token := ParagraphEndToken.parse(line):
            yield paragraph_token
            return

        for token in self._parse_line_text(line):
            yield token

    def _parse_line_text(self, line: str) -> Generator[Token, None, None]:
        def format_text(text: str) -> str:
            import re

            matches = re.findall(r'[*][*]', text)
            for i in range(len(matches) // 2):
                # Match 1
                match_1 = text.find('**')
                text = text[:match_1] + '&lt;b&gt;' + text[match_1 + 2:]

                # Match 2
                match_1 = text.find('**')
                text = text[:match_1] + '&lt;/b&gt;' + text[match_1 + 2:]

            text = text.lstrip().rstrip()

            return text

        def parse_box(items, pattern, r_i_type, text=None):
            new_list = list()
            for item, i_type in items:
                if i_type != 'text':
                    new_list.append((item, i_type))
                    continue
                match_item = item
                for i in range(item.count(pattern)):
                    match_1 = match_item.find(pattern)

                    before_text = match_item[:match_1]
                    match_item = match_item[match_1 + len(pattern):]

                    new_list.append((before_text, 'text'))
                    new_list.append((text, r_i_type))

                if match_item:
                    new_list.append((match_item, 'text'))
            return new_list

        items = [(line, 'text')]

        # Math
        new_list = list()
        for item, i_type in items:
            if i_type != 'text':
                new_list.append((item, i_type))
                continue
            match_item = item
            for i in range(item.count('$') // 2):
                match_1 = match_item.find('$')
                match_2 = match_item.find('$', match_1 + 1)

                before_text = match_item[:match_1]
                math_text = match_item[match_1:match_2 + 1][1:-1]
                match_item = match_item[match_2 + 1:]

                new_list.append((before_text, 'text'))
                new_list.append((math_text, 'math'))

            if match_item:
                new_list.append((match_item, 'text'))
        items = new_list

        # Checkboxes
        items = parse_box(items, '[]', 'checkbox_false')
        items = parse_box(items, '[x]', 'checkbox_true')

        for item, i_type in items:
            if i_type == 'text' and item and item != '':
                yield TextToken(text=format_text(item))
            elif i_type == 'math' and item:
                yield MathTextToken(text=item)
            elif i_type == 'checkbox_false':
                yield CheckBoxTextToken(value=False)
            elif i_type == 'checkbox_true':
                yield CheckBoxTextToken(value=True)

    def _walk_tokens(self, tokens: List[Token], ctx: ContextManager):

        for token in tokens:
            token.walk(ctx)

        return ctx
