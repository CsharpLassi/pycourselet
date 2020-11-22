from typing import Optional

from .context import NeedSettings
from .text_context import TextContext


class AudioTextContext(TextContext):
    def __init__(self, alt: str = None, url: str = None, **kwargs):
        super().__init__(type='audio', **kwargs)
        self.url = url
        self.alt = alt

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .paragraph_context import ParagraphContext
        from .table_contexts import TableBlockContext

        return NeedSettings(ParagraphContext, TableBlockContext)
