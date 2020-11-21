from .courselet_block import CourseletBlock


class ListBlock(CourseletBlock):
    def __init__(self, block_id: str):
        super(ListBlock, self).__init__(block_id, block_type='list')
