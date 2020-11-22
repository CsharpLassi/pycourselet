from typing import Optional

from .context import NeedSettings
from .text_context import TextContext


class CheckboxTextContext(TextContext):
    def __init__(self, value: bool = True,
                 is_exercise: int = 1, default_score: int = 1, **kwargs):
        super().__init__(type='checkbox', **kwargs)
        self.text = '1' if value else '0'

        self.is_exercise = is_exercise
        self.default_score = default_score

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .paragraph_context import ParagraphContext
        from .table_contexts import TableBlockContext
        return NeedSettings(ParagraphContext, TableBlockContext)
