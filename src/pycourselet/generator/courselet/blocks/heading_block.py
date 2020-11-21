from .courselet_block import CourseletBlock


class HeadingBlock(CourseletBlock):
    def __init__(self, block_id: str, level: int = 1):
        assert level > 0, 'level must be greater then 0'
        super(HeadingBlock, self).__init__(block_id, block_type=f'heading{level}')
