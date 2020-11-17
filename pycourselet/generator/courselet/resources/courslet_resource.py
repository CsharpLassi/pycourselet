import os
import pathlib
import re
import shutil

import wget


class CourseletResource:
    def __init__(self, resource_id: str, url: str):
        self.resource_id = resource_id
        self.suffix = ''
        self.url = url

    @property
    def file_name(self) -> str:
        file_name = str(self.resource_id)
        if self.suffix:
            file_name += f'.{self.suffix}'

        return file_name

    def download(self, dest_dir: str):
        pattern = '^[a-z]*://'

        self.suffix = pathlib.Path(self.url).suffix[1:]

        dest_path = os.path.join(dest_dir, self.resource_id + f'.{self.suffix}')

        if re.match(pattern, self.url):
            # Online
            print(f'Download: {self.url}; Suffix:{self.suffix}')
            wget.download(self.url, dest_path)

            if self.suffix == 'svg':
                from cairosvg import svg2png
                self.suffix = 'png'
                new_dest_path = os.path.join(dest_dir,
                                             self.resource_id + f'.{self.suffix}')
                svg2png(url=dest_path, write_to=new_dest_path)
                os.remove(dest_path)
            return

        # local
        shutil.copy(self.url, dest_path)
