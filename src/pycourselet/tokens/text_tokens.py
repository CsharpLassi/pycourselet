from __future__ import annotations

from collections import Generator

from .token import Token
from ..contexts import TextContext, MathTextContext, CheckboxTextContext, ContextManager


class TextToken(Token):
    def __init__(self, text: str = None):
        self.text: str = text

    def walk(self, ctx: ContextManager):
        ctx.push_create(TextContext, text=self.text)

    @staticmethod
    def parse(line: str) -> Generator[TextToken, None, None]:
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


class MathTextToken(TextToken):
    def __init__(self, text: str = None):
        super().__init__(text)

    def walk(self, ctx: ContextManager):
        ctx.push_create(MathTextContext, text=self.text)


class CheckBoxTextToken(TextToken):
    def __init__(self, value: bool = False):
        super().__init__()
        self.value = value

    def walk(self, ctx: ContextManager):
        ctx.push_create(CheckboxTextContext, value=self.value)
