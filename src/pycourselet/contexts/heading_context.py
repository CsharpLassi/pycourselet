from typing import Optional

from .block_context import BlockContext
from .context import NeedSettings
from .text_context import TextContext


class PageHeadingContext(BlockContext):
    def __init__(self, **kwargs):
        super().__init__('heading1', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .page_context import PageContext
        return NeedSettings(PageContext)


class PageHeadingTextContext(TextContext):
    def __init__(self, **kwargs):
        super().__init__(type='line', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        return NeedSettings(PageHeadingContext)


class HeadingContext(BlockContext):
    def __init__(self, **kwargs):
        super().__init__('heading2', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .page_context import PageContext
        return NeedSettings(PageContext)


class HeadingTextContext(TextContext):
    def __init__(self, **kwargs):
        super().__init__(type='line', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        return NeedSettings(HeadingContext, force_new=True)


class SubHeadingTextContext(TextContext):
    def __init__(self, **kwargs):
        super().__init__(type='heading3', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .paragraph_context import ParagraphContext
        return NeedSettings(ParagraphContext)
