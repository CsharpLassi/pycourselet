from .context import Context


class FileContext(Context):
    def __init__(self, base_file_url: str = None, **kwargs):
        super().__init__(**kwargs)
        self.base_file_url = base_file_url
