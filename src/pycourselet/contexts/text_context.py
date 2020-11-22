from typing import Optional

from .context import NeedSettings
from .element_context import ElementContext


class TextContext(ElementContext):
    def __init__(self, type: str = 'text', text: str = None, **kwargs):
        super().__init__(type, **kwargs)

        self.text: str = text

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .paragraph_context import ParagraphContext
        from .table_contexts import TableBlockContext
        return NeedSettings(ParagraphContext, TableBlockContext)
