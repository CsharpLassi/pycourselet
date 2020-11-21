from __future__ import annotations

from typing import List, Optional, Type


class Context:
    def __init__(self, **kwargs):
        self.parent: Optional[Context] = None
        self.children: List[Context] = list()

    @staticmethod
    def need() -> Optional[Type[Context]]:
        return None

    def begin(self):
        return

    def end(self):
        return


class TypeContext(Context):
    def __init__(self, type: str, **kwargs):
        super().__init__(**kwargs)
        self.type = type
