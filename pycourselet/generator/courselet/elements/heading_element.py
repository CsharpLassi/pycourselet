from typing import Optional

from .text_element import TextElement


class HeadingElement(TextElement):
    def __init__(self, element_id: str, level: int = 1, text: Optional[str] = None):
        assert level > 0, 'level must be greater then 0'
        
        super(HeadingElement, self).__init__(element_id, text=text,
                                             element_type=f'heading{level}')
