from .context import TypeContext

block_id = 0


class BlockContext(TypeContext):
    def __init__(self, type: str, **kwargs):
        global block_id
        super(BlockContext, self).__init__(type, **kwargs)

        block_id += 1

        self.id = f'Block_{block_id}'
