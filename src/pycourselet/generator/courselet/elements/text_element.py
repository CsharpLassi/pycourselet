import xml.etree.ElementTree as et
from typing import Optional

from .courselet_element import CourseletElement


class TextElement(CourseletElement):
    def __init__(self, element_id: str, text: Optional[str] = None,
                 element_type: str = 'text'):
        super(TextElement, self).__init__(element_id, element_type=element_type)
        self.text = text

    def _on_create(self, element: et.Element):
        element.text = self.text
