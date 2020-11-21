import xml.etree.ElementTree as et

from .courselet_block import CourseletBlock


class MetaBlock(CourseletBlock):
    def __init__(self, block_id: str, title: str = 'PageTitle'):
        super(MetaBlock, self).__init__(block_id, block_type='meta')

        self.title = title
        self.link_next_page: str = 'after_attempt'
        self.overview: str = 'score score_max'
        self.attempts: str = 'unlimited'
        self.feedback: int = 1

    def _on_create(self, block: et.Element):
        block.attrib['title'] = self.title
        block.attrib['link_next_page'] = self.link_next_page
        block.attrib['overview'] = self.overview
        block.attrib['attempts'] = self.attempts
        block.attrib['feedback'] = str(self.feedback)
