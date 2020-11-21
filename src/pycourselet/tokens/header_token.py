from __future__ import annotations

from typing import Optional


class HeaderToken:
    def __init__(self, level: int, text: str):
        self.level = level
        self.text = text

    @staticmethod
    def parse(source: str) -> Optional[HeaderToken]:
        levels = ['# ', '## ', '### ', '#### ', '##### ', '###### ']

        for i, pattern in enumerate(levels):
            level = i + 1
            if source.startswith(pattern) and source != pattern:
                text = source[len(pattern):]
                text = text.lstrip().rstrip()
                return HeaderToken(level, text)
