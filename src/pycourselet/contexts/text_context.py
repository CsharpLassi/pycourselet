from pycourselet.contexts import ElementContext


class TextContext(ElementContext):
    def __init__(self, type: str = 'text', text: str = None, **kwargs):
        super().__init__(type, **kwargs)

        self.text: str = text
