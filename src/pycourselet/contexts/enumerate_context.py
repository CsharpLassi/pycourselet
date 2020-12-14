from typing import Optional

from .block_context import BlockContext
from .context import NeedSettings
from .text_context import TextContext


class EnumerateContext(BlockContext):
    def __init__(self, **kwargs):
        super().__init__('paragraph', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .page_context import PageContext
        return NeedSettings(PageContext)


class EnumerateHeadingContext(TextContext):
    def __init__(self, level: int = 0, **kwargs):
        super().__init__(type='heading3', **kwargs)

        self.level = level

    @staticmethod
    def need() -> Optional[NeedSettings]:
        return NeedSettings(EnumerateContext, force_new=True)
