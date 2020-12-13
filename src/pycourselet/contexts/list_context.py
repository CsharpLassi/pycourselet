from typing import Optional

from .block_context import BlockContext
from .context import NeedSettings
from .text_context import TextContext


class ListContext(BlockContext):
    def __init__(self, **kwargs):
        super().__init__('list', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .page_context import PageContext
        return NeedSettings(PageContext)


class ListHeadingContext(TextContext):
    def __init__(self, **kwargs):
        super().__init__(type='heading3', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        return NeedSettings(ListContext, force_new=True)
