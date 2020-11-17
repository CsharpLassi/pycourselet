import xml.etree.ElementTree as et

from typing import Optional, TypeVar, Type, List

# noinspection PyTypeChecker
B = TypeVar('B', bound="CourseletBlock")


class CourseletBlock:
    def __init__(self, block_id: str, block_type: Optional[str] = None):
        self.block_id = block_id
        self.block_type = block_type

        self.current_element_id_number: int = 0
        self.elements: List[CourseletElement] = list()

    def add_element(self, block_type: Type[B], *args, **kwargs) -> B:
        element = block_type(self.next_element_id(), *args, **kwargs)
        self.elements.append(element)
        return element

    def next_element_id(self) -> str:
        self.current_element_id_number += 1
        return f'{self.block_id}_e{self.current_element_id_number}'

    def create(self) -> Optional[et.Element]:
        if not self.block_type:
            return
        block = et.Element('block')
        block.attrib['id'] = self.block_id
        block.attrib['type'] = self.block_type

        # Elements
        for element in self.elements:
            block.append(element.create())

        self._on_create(block)

        return block

    def _on_create(self, block: et.Element):
        pass
