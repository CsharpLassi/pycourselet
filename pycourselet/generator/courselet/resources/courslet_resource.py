import os
import re
import shutil

import wget


class CourseletResource:
    def __init__(self, resource_id: str, url: str):
        self.resource_id = resource_id
        self.url = url

    def download(self, dest_dir: str):
        pattern = '^[a-z]*://'

        dest_path = os.path.join(dest_dir, self.resource_id)

        if re.match(pattern, self.url):
            # Online
            wget.download(self.url, dest_path)
            return

        # local
        shutil.copy(self.url, dest_path)
