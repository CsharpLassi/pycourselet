from typing import Optional

from .block_context import BlockContext
from .context import NeedSettings
from .element_context import ElementContext


class EnumerateContext(BlockContext):
    def __init__(self, **kwargs):
        super().__init__('paragraph', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .page_context import PageContext
        return NeedSettings(PageContext)


class EnumerateHeadingContext(ElementContext):
    def __init__(self, level: int = 0, **kwargs):
        super().__init__(type='text', **kwargs)

        self.level = level

    @staticmethod
    def need() -> Optional[NeedSettings]:
        return NeedSettings(EnumerateContext, force_new=True)
