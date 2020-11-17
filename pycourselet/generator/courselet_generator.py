from __future__ import annotations

import os
import re
from typing import Dict, Generator, Optional, List

from .courselet.blocks import *
from .courselet.elements import *
from .courselet.pages import *
from .courselet.resources import *


def parser_method(func):
    def wrapper(self, *args, **kwargs):
        kwargs['is_continue'] = self._last_method == func.__name__
        self._last_method = func.__name__
        return func(self, *args, **kwargs)

    return wrapper


def _parse_text(block: CourseletBlock, text: str):
    def _parse_box(items, pattern, r_i_type, text=None):
        new_list = list()
        for item, i_type in items:
            if i_type != 'text':
                new_list.append((item, i_type))
                continue
            match_item = item
            for i in range(item.count(pattern)):
                match_1 = match_item.find(pattern)

                before_text = match_item[:match_1]
                match_item = match_item[match_1 + len(pattern):]

                new_list.append((before_text, 'text'))
                new_list.append((text, r_i_type))

            if match_item:
                new_list.append((match_item, 'text'))
        return new_list

    items = [(text, 'text')]

    # Math
    new_list = list()
    for item, i_type in items:
        if i_type != 'text':
            new_list.append((item, i_type))
            continue
        match_item = item
        for i in range(item.count('$') // 2):
            match_1 = match_item.find('$')
            match_2 = match_item.find('$', match_1 + 1)

            before_text = match_item[:match_1]
            math_text = match_item[match_1:match_2 + 1][1:-1]
            match_item = match_item[match_2 + 1:]

            new_list.append((before_text, 'text'))
            new_list.append((math_text, 'math'))

        if match_item:
            new_list.append((match_item, 'text'))
    items = new_list

    # Checkboxes
    items = _parse_box(items, '[]', 'checkbox_false')
    items = _parse_box(items, '[x]', 'checkbox_true')

    for item, i_type in items:
        if i_type == 'text' and item:
            block.add_element(TextElement, text=_format_text(item))
        elif i_type == 'math' and item:
            block.add_element(MathElement, text=item)
        elif i_type == 'checkbox_false':
            block.add_element(CheckBoxElement, true_false=False)
        elif i_type == 'checkbox_true':
            block.add_element(CheckBoxElement, true_false=True)

    return


def _format_text(text: str) -> str:
    import re

    matches = re.findall(r'[*][*]', text)
    for i in range(len(matches) // 2):
        # Match 1
        match_1 = text.find('**')
        text = text[:match_1] + '&lt;b&gt;' + text[match_1 + 2:]

        # Match 2
        match_1 = text.find('**')
        text = text[:match_1] + '&lt;/b&gt;' + text[match_1 + 2:]
    return text


def _split_math(text: str) -> Generator[str, None, None]:
    if (count := text.count('$')) >= 2:
        for i in range(count // 2):
            match_1 = text.find('$')
            match_2 = text.find('$', match_1 + 1)

            before_text = text[:match_1]
            math_text = text[match_1:match_2 + 1]
            text = text[match_2 + 1:]
            if before_text:
                yield before_text

            yield math_text

    if text:
        yield text


class CourseletGenerator:

    def __init__(self):
        self.current_page_id_number: int = 0
        self.pages: Dict[str, CourseletPage] = dict()
        self.current_page: Optional[CourseletPage] = None
        self.create_new_page()

        self.current_resource_id_number: int = 0
        self.resources: Dict[str, CourseletResource] = dict()

        self._line_break: bool = False
        self._last_method: Optional[str] = None
        self._continue_count: int = 0

    def add_resource(self, url: str) -> CourseletResource:
        self.current_resource_id_number += 1
        resource_id: str = f'r{self.current_resource_id_number}'

        resource = CourseletResource(resource_id, url)
        self.resources[resource_id] = resource

        return resource

    def create_new_page(self, title: str = 'Start',
                        change_title: bool = True) -> CourseletPage:
        if not self.current_page_id_number or len(self.current_page.blocks) > 1:
            self.current_page_id_number += 1
            new_name: str = f'p{self.current_page_id_number}'
            new_page: CourseletPage = CourseletPage(new_name, title)
            self.pages[new_name] = new_page
            self.current_page = new_page
        elif change_title:
            self.current_page.meta.title = title
        return self.current_page

    def add_text(self, text: str, file_path: Optional[str] = None):
        lines: List[str] = text.splitlines()

        if not lines:
            self._last_method = None
            self._continue_count = 0
            self._line_break = True
            return

        for line in lines:
            if not line:
                self._line_break = True
                self._last_method = None
                self._continue_count = 0
                continue
            self._continue_count += 1
            line = line.strip()
            # Todo: wrong place

            self._parse_line(line, file_path=file_path)
            self._line_break = False

    def import_directory(self, dir_path: str):
        def key_function(key):
            if (i := key.find('_')) >= 0:
                key = key[:i]
            return key

        list_dir = os.listdir(dir_path)
        sorted_list_dir = sorted(list_dir, key=key_function)
        for item_name in sorted_list_dir:
            item_path = os.path.join(dir_path, item_name)
            if os.path.isfile(item_path):
                title = item_name
                if (i := title.find('_')) >= 0:
                    title = title[i + 1:]
                if (i := title.rfind('.')) >= 0:
                    title = title[:i]
                self.create_new_page(title)
                with open(item_path, 'r') as fs:
                    for line in fs:
                        line = line.rstrip()
                        self.add_text(line, file_path=item_path)

    def write_to(self, name: str, output_file: str):
        import xml.etree.ElementTree as et
        import tempfile
        import shutil

        with tempfile.TemporaryDirectory(prefix='exschool_') as tmp_dirname:
            courselet_element = et.Element('courselet')
            meta = et.SubElement(courselet_element, 'meta')
            pages = et.SubElement(courselet_element, 'pages')

            # Metas
            general = et.SubElement(meta, 'general')
            et.SubElement(general, 'title').text = name
            et.SubElement(general, 'mapping').text = '0'

            page_dir = os.path.join(tmp_dirname, 'pages')
            os.mkdir(page_dir)
            for page_id, page in self.pages.items():
                page_element = et.SubElement(pages, 'page')
                page_element.attrib['id'] = page_id
                page_element.attrib['title'] = page.meta.title
                page_element.attrib['overview'] = page.meta.overview
                page_element.attrib['href'] = os.path.join('pages', f'{page_id}.xml')
                page.write_to(page_dir)

            if len(self.resources) > 0:
                resources = et.SubElement(courselet_element, 'resources')

                resources_dir = os.path.join(tmp_dirname, 'resources')
                os.mkdir(resources_dir)

                for resource_id, resource in self.resources.items():
                    resource.download(resources_dir)

                    resource_element = et.SubElement(resources, 'resource')
                    resource_element.attrib['id'] = resource_id
                    resource_element.attrib['href'] = os.path.join('resources',
                                                                   f'{resource.file_name}')

            root = et.ElementTree(courselet_element)
            root.write(os.path.join(tmp_dirname, f'courselet.xml'),
                       xml_declaration=True, encoding='UTF-8')

            if output_file.endswith('.zip'):
                output_file = output_file[:-4]
            shutil.make_archive(output_file, 'zip', tmp_dirname)

    def _parse_line(self, line: str, file_path: Optional[str] = None):
        parse_list = dict()

        # Headers
        parse_list['# '] = lambda t: self._parse_header(t, 1)
        parse_list['## '] = lambda t: self._parse_header(t, 2)
        parse_list['### '] = lambda t: self._parse_header(t, 3)
        parse_list['#### '] = lambda t: self._parse_header(t, 4)

        # Cite
        parse_list['>'] = lambda t: self._parse_cite(t)

        # List
        parse_list['-'] = lambda t: self._parse_list(t)

        # Pictures
        parse_list['!'] = lambda t: self._parse_picture(t, file_path=file_path)

        for key, method in parse_list.items():
            if line.startswith(key):
                t = line[len(key):].strip()
                method(t)
                return

        # Test Tables
        if line.startswith('|') and line.endswith('|'):
            self._parse_table(line)
            return

        # Test Math
        if line.startswith('$') and line.endswith('$'):
            self._parse_math(line)
            return

        self._parse_text(line)

    @parser_method
    def _parse_header(self, text: str, level: int, **kwargs):
        if level == 1:
            self.create_new_page(title=text)

        if level in [1, 2]:
            block = self.current_page.add_block(HeadingBlock, level=level)
            block.add_element(LineElement, text=text)
        else:
            block = self.current_page.add_block(ParagraphBlock)
            block.add_element(HeadingElement, level=3, text=text)

    @parser_method
    def _parse_cite(self, text: str, **kwargs):

        if isinstance(lb := self.current_page.last_block(), CiteBlock):
            lb.add_element(TextElement, text=text)
            return

        header_text = None
        if (i := text.find(':')) >= 0:
            header_text = text[:i].rstrip()
            text = text[i + 1:].strip()

        block = self.current_page.add_block(CiteBlock)

        block.add_element(HeadingElement, level=3, text=header_text)

        _parse_text(block, text)

        return block

    @parser_method
    def _parse_list(self, text: str, **kwargs):
        text = _format_text(text)

        block = self.current_page.add_block(ListBlock)
        block.add_element(HeadingElement, level=3, text=text)

    @parser_method
    def _parse_picture(self, text: str, file_path: Optional[str] = None, **kwargs):
        import re
        pattern = r'^\[(?P<alt>.*)\]\(\"?(?P<url>.*?)\"?( \"(?P<title>.*)\")?\)$'
        url_pattern = r'^[a-z]*://'

        match = re.match(pattern, text)

        if not match:
            self._parse_text(text)
            return

        alt_text = match.group('alt')
        title = match.group('title')
        url = match.group('url')

        is_online = re.match(url_pattern, url)

        if url.startswith('./'):
            url = url[2:]

        if file_path and not is_online:
            base_url = os.path.dirname(file_path)
            url = os.path.join(base_url, url)

        resource = self.add_resource(url)
        block = self.current_page.add_block(ImageBlock, resource, alt_text)

        if is_online:
            block.add_element(TextElement, text=f'Quelle:{url}')

    @parser_method
    def _parse_text(self, text: str, is_continue: bool = False, **kwargs):
        text = _format_text(text)

        lb = self.current_page.last_block()

        if not (not self._line_break and isinstance(lb, ParagraphBlock)):
            lb = self.current_page.add_block(ParagraphBlock)

        _parse_text(lb, text)

    @parser_method
    def _parse_table(self, text: str, is_continue: bool = False, **kwargs):
        if is_continue and self._continue_count == 2:
            return

        block = self.current_page.last_block()

        if not (isinstance(block, TableBlock)):
            block = self.current_page.add_block(TableBlock)

        if self._continue_count > 1:
            block.add_element(TableRowBreakElement)

        rows = [row.replace('\\|', '|').strip().rstrip()
                for row in re.split(r'(?<!\\)\|', text)[1:-1]]
        for i, row in enumerate(rows):
            _parse_text(block, row)
            if i == len(rows) - 1:
                continue
            block.add_element(TableColumnBreakElement)

        return

    @parser_method
    def _parse_math(self, text: str, **kwargs):
        text = text[1:-1]

        block = self.current_page.last_block()

        if self._line_break or not (isinstance(block, ParagraphBlock)):
            block = self.current_page.add_block(ParagraphBlock)

        block.add_element(MathElement, text=text)

        return
