from typing import Optional, Type

from pycourselet.contexts import Context, TypeContext
from .text_context import TextContext


class PageHeadingContext(TypeContext):
    def __init__(self, **kwargs):
        super().__init__('heading1', **kwargs)

    @staticmethod
    def need() -> Optional[Type[Context]]:
        from .page_context import PageContext
        return PageContext


class PageHeadingTextContext(TextContext):
    def __init__(self, **kwargs):
        super().__init__(type='line', **kwargs)

    @staticmethod
    def need() -> Optional[Type[Context]]:
        return PageHeadingContext
