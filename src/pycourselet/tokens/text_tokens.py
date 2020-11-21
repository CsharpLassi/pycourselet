from .token import Token
from ..contexts import TextContext, MathTextContext, CheckboxTextContext, ContextManager


class TextToken(Token):
    def __init__(self, text: str = None):
        self.text: str = text

    def walk(self, ctx: ContextManager):
        ctx.push_create(TextContext, text=self.text)


class MathTextToken(Token):
    def __init__(self, text: str = None):
        self.text: str = text

    def walk(self, ctx: ContextManager):
        ctx.push_create(MathTextContext, text=self.text)


class CheckBoxTextToken(Token):
    def __init__(self, value: bool = False):
        self.value = value

    def walk(self, ctx: ContextManager):
        ctx.push_create(CheckboxTextContext, value=self.value)
