from .context import TypeContext

element_id = 0


class ElementContext(TypeContext):
    def __init__(self, type: str, **kwargs):
        global element_id
        super(ElementContext, self).__init__(type, **kwargs)

        element_id += 1

        self.id = f'Element_{element_id}'
