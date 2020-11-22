from typing import Optional

from .block_context import BlockContext
from .context import NeedSettings


class ImageContext(BlockContext):
    def __init__(self, alt_text: str, title: str, url: str, **kwargs):
        super().__init__('image', **kwargs)
        self.url = url
        self.title = title
        self.alt_text = alt_text

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .page_context import PageContext
        return NeedSettings(PageContext)
