import xml.etree.ElementTree as et

from .courselet_element import CourseletElement


class LinkElement(CourseletElement):
    def __init__(self, element_id: str, url: str, text: str):
        super(LinkElement, self).__init__(element_id, element_type='link')
        self.url = url
        self.text = text

    def _on_create(self, element: et.Element):
        element.attrib['url'] = self.url
        element.text = self.text
