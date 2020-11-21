import xml.etree.ElementTree as et

from .courselet_block import CourseletBlock


class TableBlock(CourseletBlock):
    def __init__(self, block_id: str):
        super(TableBlock, self).__init__(block_id, block_type='table')

    def _on_create(self, block: et.Element):
        block.attrib['image_sizing'] = 'cover'
