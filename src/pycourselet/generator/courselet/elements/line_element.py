from typing import Optional

from .text_element import TextElement


class LineElement(TextElement):
    def __init__(self, element_id: str, text: Optional[str] = None):
        super(LineElement, self).__init__(element_id, text=text, element_type='line')
