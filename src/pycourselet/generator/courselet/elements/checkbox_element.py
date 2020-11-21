import xml.etree.ElementTree as et

from .text_element import TextElement


class CheckBoxElement(TextElement):
    def __init__(self, element_id: str, true_false: bool = False):
        text = '1' if true_false else '0'
        super(CheckBoxElement, self).__init__(element_id,
                                              text=text,
                                              element_type='checkbox')
        self.is_exercise = 1
        self.default_score = 1

    def _on_create(self, element: et.Element):
        element.attrib['is_exercise'] = str(self.is_exercise)
        element.attrib['default_score'] = str(self.default_score)
        element.text = self.text
