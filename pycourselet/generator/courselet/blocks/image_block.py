import xml.etree.ElementTree as et

from ..resources import CourseletResource
from .courselet_block import CourseletBlock


class ImageBlock(CourseletBlock):
    def __init__(self, block_id: str, resource: CourseletResource, alt: str):
        super(ImageBlock, self).__init__(block_id, block_type='image')
        self.resource = resource
        self.alt = alt

    def _on_create(self, block: et.Element):
        block.attrib['alt'] = self.alt
        block.attrib['image_idref'] = self.resource.resource_id
