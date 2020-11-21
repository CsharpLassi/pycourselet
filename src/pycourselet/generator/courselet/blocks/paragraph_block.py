from .courselet_block import CourseletBlock


class ParagraphBlock(CourseletBlock):
    def __init__(self, block_id: str):
        super(ParagraphBlock, self).__init__(block_id, block_type='paragraph')
