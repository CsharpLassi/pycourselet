from typing import Optional, Type

from .block_context import BlockContext
from .context import NeedSettings


class ParagraphContext(BlockContext):
    def __init__(self, **kwargs):
        super().__init__('paragraph', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .page_context import PageContext
        return NeedSettings(PageContext)
