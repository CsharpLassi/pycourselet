from pycourselet.contexts import TypeContext


class TextContext(TypeContext):
    def __init__(self, type: str = 'text', **kwargs):
        super().__init__(type, **kwargs)

        self.text: str = None
