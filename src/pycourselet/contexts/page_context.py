from .context import Context

page_id = 0


class PageContext(Context):
    def __init__(self, title: str = None, **kwargs):
        global page_id
        super().__init__(**kwargs)

        page_id += 1

        self.name = f'Page_{page_id}'

        self.title = title if title else self.name

        self.link_next_page: str = 'after_attempt'
        self.overview: str = 'score score_max'
        self.attempts: str = 'unlimited'
        self.feedback: int = 1
