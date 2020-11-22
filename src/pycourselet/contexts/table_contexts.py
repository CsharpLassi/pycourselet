from typing import Optional

from .block_context import BlockContext
from .context import NeedSettings
from .element_context import ElementContext


class TableBlockContext(BlockContext):
    def __init__(self, **kwargs):
        super().__init__('table', **kwargs)
        self.image_sizing: str = 'cover'

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .page_context import PageContext
        return NeedSettings(PageContext)


class TableColumnBreakContext(ElementContext):
    def __init__(self, **kwargs):
        super().__init__(type='table_column_break', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        return NeedSettings(TableBlockContext)


class TableRowBreakContext(ElementContext):
    def __init__(self, **kwargs):
        super().__init__(type='table_row_break', **kwargs)

    @staticmethod
    def need() -> Optional[NeedSettings]:
        return NeedSettings(TableBlockContext)
