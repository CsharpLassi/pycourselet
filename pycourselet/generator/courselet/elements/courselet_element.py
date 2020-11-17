import xml.etree.ElementTree as et
from typing import Optional


class CourseletElement:
    def __init__(self, element_id: str, element_type: Optional[str] = None):
        self.element_type = element_type
        self.element_id = element_id

    def create(self) -> Optional[et.Element]:
        if not self.element_type:
            return
        element = et.Element('element')
        element.attrib['id'] = self.element_id
        element.attrib['type'] = self.element_type

        self._on_create(element)

        return element

    def _on_create(self, element: et.Element):
        pass
