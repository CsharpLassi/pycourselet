import os
import xml.etree.ElementTree as et

from typing import List, TypeVar, Type, Optional

from ..blocks import CourseletBlock, MetaBlock

B = TypeVar('B', bound=CourseletBlock)


class CourseletPage:
    def __init__(self, page_id: str, title: str):
        self.page_id: str = page_id

        self.current_block_id_number: int = 0
        self.blocks: List[CourseletBlock] = list()

        self.meta: MetaBlock = self.add_block(MetaBlock, title=title)

    def next_block_id(self) -> str:
        self.current_block_id_number += 1
        return f'{self.page_id}_b{self.current_block_id_number}'

    def add_block(self, block_type: Type[B], *args, **kwargs) -> B:
        block = block_type(self.next_block_id(), *args, **kwargs)
        self.blocks.append(block)
        return block

    def last_block(self) -> Optional[CourseletBlock]:
        if len(self.blocks) > 0:
            return self.blocks[-1]
        return None

    def create(self) -> et.Element:
        page_element = et.Element('page')
        page_element.attrib['id'] = self.page_id

        page_contents = et.SubElement(page_element, 'contents')
        for block in self.blocks:
            page_contents.append(block.create())

        return page_element

    def write_to(self, dir_name: str):
        root = et.ElementTree(self.create())
        root.write(os.path.join(dir_name, f'{self.page_id}.xml'),
                   xml_declaration=True, encoding='UTF-8')
