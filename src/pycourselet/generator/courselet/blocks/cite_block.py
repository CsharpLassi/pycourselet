from .courselet_block import CourseletBlock


class CiteBlock(CourseletBlock):
    def __init__(self, block_id: str):
        super(CiteBlock, self).__init__(block_id, block_type='box')
