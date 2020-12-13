from __future__ import annotations

import re
from typing import Optional

from .token import Token
from ..contexts import ContextManager


class ImageToken(Token):
    def __init__(self, alt_text: str, title: str, url: str):
        self.url = url
        self.title = title
        self.alt_text = alt_text

    def walk(self, ctx: ContextManager):
        from ..contexts import ImageContext
        ctx.push_create(ImageContext,
                        alt_text=self.alt_text,
                        title=self.title,
                        url=self.url)

    @staticmethod
    def parse(source: str) -> Optional[ImageToken]:
        source = source.lstrip().rstrip()

        pattern = r'^!\[(?P<alt>.*)\]\(\"?(?P<url>.*?)\"?( \"(?P<title>.*)\")?\)$'

        match = re.match(pattern, source)

        if not match:
            return

        alt_text = match.group('alt')
        title = match.group('title')
        url = match.group('url')

        return ImageToken(alt_text, title, url)
