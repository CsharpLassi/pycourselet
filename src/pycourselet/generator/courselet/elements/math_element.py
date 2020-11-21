import xml.etree.ElementTree as et

from typing import Optional

from .text_element import TextElement


class MathElement(TextElement):
    def __init__(self, element_id: str, text: Optional[str] = None):
        super(MathElement, self).__init__(element_id, text=text, element_type='math')
        self.mode = 'tex'

    def _on_create(self, element: et.Element):
        element.attrib['mode'] = self.mode
        element.text = self.text
