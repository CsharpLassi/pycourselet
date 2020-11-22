import os
import pathlib
import re
import shutil
import tempfile
import xml.etree.ElementTree as et
from typing import Optional, List

import wget

from .contexts import *


class CourseletContextCompiler:
    def compile_context(self, ctx: ContextManager, **kwargs):
        self.begin(ctx, **kwargs)

        for base in ctx.base:
            self._listen_context(base, ctx, **kwargs)

        self.end(ctx, **kwargs)

    def begin(self, ctx: ContextManager, **kwargs):
        return

    def end(self, ctx: ContextManager, **kwargs):
        return

    def _listen_context(self, context: Context, ctx: ContextManager, **kwargs):
        methods = {
            FileContext: (
                self.begin_file_context,
                self.end_file_context),
            PageContext: (
                self.begin_page_context,
                self.end_page_context),
            PageHeadingContext: (
                self.begin_page_heading_context,
                self.end_page_heading_context),
            PageHeadingTextContext: (
                self.begin_page_heading_text_context,
                self.end_page_heading_text_context),
            HeadingContext: (
                self.begin_heading_context,
                self.end_heading_context),
            HeadingTextContext: (
                self.begin_heading_text_context,
                self.end_heading_text_context),
            SubHeadingTextContext: (
                self.begin_sub_heading_text_context,
                self.end_sub_heading_text_context),
            ParagraphContext: (
                self.begin_paragraph_context,
                self.end_paragraph_context),
            TextContext: (
                self.begin_text_context,
                self.end_text_context),
            MathTextContext: (
                self.begin_math_text_context,
                self.end_math_text_context),
            CheckboxTextContext: (
                self.begin_checkbox_text_context,
                self.end_checkbox_text_context),
            ImageContext: (
                self.begin_image_context,
                self.end_image_context),
            ListContext: (
                self.begin_list_context,
                self.end_list_context),
            ListHeadingContext: (
                self.begin_list_heading_context,
                self.end_list_heading_context),
            TableBlockContext: (
                self.begin_table_block_context,
                self.end_table_block_context),
            TableColumnBreakContext: (
                self.begin_table_column_break_context,
                self.end_table_column_break_context),
            TableRowBreakContext: (
                self.begin_table_row_break_context,
                self.end_table_row_break_context),
            AudioTextContext: (
                self.begin_audio_context,
                self.end_audio_context),
        }

        context_type = type(context)

        if context_type in methods:
            methods[context_type][0](context, **kwargs)

        for child in context.children:
            self._listen_context(child, ctx, **kwargs)

        if context_type in methods:
            methods[context_type][1](context, **kwargs)

    def begin_file_context(self, context: FileContext, **kwargs):
        return

    def end_file_context(self, context: FileContext, **kwargs):
        return

    def begin_page_context(self, context: PageContext, **kwargs):
        return

    def end_page_context(self, context: PageContext, **kwargs):
        return

    def begin_page_heading_context(self, context: PageHeadingContext, **kwargs):
        return

    def end_page_heading_context(self, context: PageHeadingContext, **kwargs):
        return

    def begin_page_heading_text_context(self, context: PageHeadingTextContext,
                                        **kwargs):
        return

    def end_page_heading_text_context(self, context: PageHeadingTextContext, **kwargs):
        return

    def begin_heading_context(self, context: HeadingContext, **kwargs):
        return

    def end_heading_context(self, context: HeadingContext, **kwargs):
        return

    def begin_heading_text_context(self, context: HeadingTextContext,
                                   **kwargs):
        return

    def end_heading_text_context(self, context: HeadingTextContext, **kwargs):
        return

    def begin_sub_heading_text_context(self, context: SubHeadingTextContext,
                                       **kwargs):
        return

    def end_sub_heading_text_context(self, context: SubHeadingTextContext, **kwargs):
        return

    def begin_text_context(self, context: TextContext, **kwargs):
        return

    def end_text_context(self, context: TextContext, **kwargs):
        return

    def begin_math_text_context(self, context: MathTextContext, **kwargs):
        return

    def end_math_text_context(self, context: MathTextContext, **kwargs):
        return

    def begin_checkbox_text_context(self, context: CheckboxTextContext, **kwargs):
        return

    def end_checkbox_text_context(self, context: CheckboxTextContext, **kwargs):
        return

    def begin_paragraph_context(self, context: ParagraphContext, **kwargs):
        return

    def end_paragraph_context(self, context: ParagraphContext, **kwargs):
        return

    def begin_image_context(self, context: ImageContext, **kwargs):
        return

    def end_image_context(self, context: ImageContext, **kwargs):
        return

    def begin_list_context(self, context: ListContext, **kwargs):
        return

    def end_list_context(self, context: ListContext, **kwargs):
        return

    def begin_list_heading_context(self, context: ListHeadingContext, **kwargs):
        return

    def end_list_heading_context(self, context: ListHeadingContext, **kwargs):
        return

    def begin_table_block_context(self, context: TableBlockContext, **kwargs):
        return

    def end_table_block_context(self, context: TableBlockContext, **kwargs):
        return

    def begin_table_column_break_context(self, context: TableColumnBreakContext,
                                         **kwargs):
        return

    def end_table_column_break_context(self, context: TableColumnBreakContext,
                                       **kwargs):
        return

    def begin_table_row_break_context(self, context: TableRowBreakContext,
                                      **kwargs):
        return

    def end_table_row_break_context(self, context: TableRowBreakContext,
                                    **kwargs):
        return

    def begin_audio_context(self, context: AudioTextContext,
                            **kwargs):
        return

    def end_audio_context(self, context: TableRowBreakContext,
                          **kwargs):
        return


class CourseletXmlContextCompiler(CourseletContextCompiler):
    def __init__(self, name: str, output_file: str):
        self.name = name
        self.output_file = output_file

        self.current_file_path: Optional[str] = None

        self.resource_id: int = 0

        self.build_dir = tempfile.TemporaryDirectory(prefix='pycourselet_').name
        self.page_dir = os.path.join(self.build_dir, 'pages')
        self.resources_dir = os.path.join(self.build_dir, 'resources')

        self.courselet_element: et.Element = et.Element('courselet')
        self.meta: et.Element = et.SubElement(self.courselet_element, 'meta')
        self.pages: et.Element = et.SubElement(self.courselet_element, 'pages')

        self.page_stack: List[et.Element] = list()

        self.current_page: Optional[et.Element] = None
        self.current_page_content: Optional[et.Element] = None

        self.resources: et.Element = et.SubElement(self.courselet_element, 'resources')

        self.current_page_block: Optional[et.Element] = None

    def begin(self, ctx: ContextManager, **kwargs):
        # Metas
        general = et.SubElement(self.meta, 'general')
        et.SubElement(general, 'title').text = self.name
        et.SubElement(general, 'mapping').text = '0'

        # Pages
        os.makedirs(self.page_dir, exist_ok=True)

        # Resources
        os.makedirs(self.resources_dir, exist_ok=True)

    def end(self, ctx: ContextManager, **kwargs):
        root = et.ElementTree(self.courselet_element)
        root.write(os.path.join(self.build_dir, f'courselet.xml'),
                   xml_declaration=True, encoding='UTF-8')

        output_file = self.output_file
        if output_file.endswith('.zip'):
            output_file = self.output_file[:-4]
        shutil.make_archive(output_file, 'zip', self.build_dir)

    def _create_block(self, context: BlockContext,
                      page_content=None) -> et.Element:
        if not page_content:
            page_content = self.current_page_content

        block = et.SubElement(page_content, 'block')
        block.attrib['id'] = context.id
        block.attrib['type'] = context.type
        return block

    def _create_element(self, context: ElementContext,
                        block=None) -> et.Element:
        if not block:
            block = self.current_page_block

        element = et.SubElement(block, 'element')
        element.attrib['id'] = context.id
        element.attrib['type'] = context.type
        return element

    def begin_file_context(self, context: FileContext, **kwargs):
        self.current_file_path = context.base_file_url

    def begin_page_context(self, context: PageContext, **kwargs):
        page_element = et.SubElement(self.pages, 'page')
        page_element.attrib['id'] = context.name
        page_element.attrib['title'] = context.title
        page_element.attrib['overview'] = context.overview
        page_element.attrib['href'] = os.path.join('pages', f'{context.name}.xml')

        self.current_page = et.Element('page')
        self.current_page.attrib['id'] = context.name

        self.current_page_content = et.SubElement(self.current_page, 'contents')
        # Meta Block
        meta_block = et.SubElement(self.current_page_content, 'block')
        meta_block.attrib['id'] = f'{context.name}_Meta'
        meta_block.attrib['type'] = 'meta'
        meta_block.attrib['title'] = context.title
        meta_block.attrib['link_next_page'] = context.link_next_page
        meta_block.attrib['overview'] = context.overview
        meta_block.attrib['attempts'] = context.attempts
        meta_block.attrib['feedback'] = str(context.feedback)

        self.page_stack.append(self.current_page)

    def end_page_context(self, context: PageContext, **kwargs):
        page_context = self.page_stack.pop()
        if page_context:
            root = et.ElementTree(page_context)
            root.write(os.path.join(self.page_dir, f'{context.name}.xml'),
                       xml_declaration=True, encoding='UTF-8')

    # Page Heading
    def begin_page_heading_context(self, context: PageHeadingContext, **kwargs):
        block = self._create_block(context)
        self.current_page_block = block

    def begin_page_heading_text_context(self, context: PageHeadingTextContext,
                                        **kwargs):
        element = self._create_element(context)
        element.text = context.text

    # Paragraphs
    def begin_paragraph_context(self, context: ParagraphContext,
                                **kwargs):
        block = self._create_block(context)
        self.current_page_block = block

    # Text
    def begin_text_context(self, context: TextContext, **kwargs):
        if not context.text:
            return
        element = self._create_element(context)
        element.text = context.text

    def begin_math_text_context(self, context: MathTextContext, **kwargs):
        if not context.text:
            return
        element = self._create_element(context)
        element.attrib['mode'] = context.mode
        element.text = context.text

    def begin_checkbox_text_context(self, context: CheckboxTextContext, **kwargs):
        element = self._create_element(context)
        element.attrib['is_exercise'] = str(context.is_exercise)
        element.attrib['default_score'] = str(context.default_score)
        element.text = context.text

    # Heading
    def begin_heading_context(self, context: HeadingContext, **kwargs):
        block = self._create_block(context)
        self.current_page_block = block

    def begin_heading_text_context(self, context: HeadingTextContext,
                                   **kwargs):
        element = self._create_element(context)
        element.text = context.text

    def begin_sub_heading_text_context(self, context: SubHeadingTextContext,
                                       **kwargs):
        element = self._create_element(context)
        element.text = context.text

    # list
    def begin_list_context(self, context: ListContext, **kwargs):
        block = self._create_block(context)
        self.current_page_block = block

    def begin_list_heading_context(self, context: ListHeadingContext, **kwargs):
        element = self._create_element(context)
        element.text = context.text

    # Image
    def begin_image_context(self, context: ImageContext,
                            **kwargs):
        block = self._create_block(context)
        self.current_page_block = block

        block.attrib['alt'] = context.alt_text

        url_pattern = r'^[a-z]*://'
        is_online = re.match(url_pattern, context.url)

        url = context.url

        if url.startswith('./'):
            url = url[2:]

        if self.current_file_path and not is_online:
            base_url = os.path.dirname(self.current_file_path)
            url = os.path.join(base_url, url)

        suffix = pathlib.Path(url).suffix[1:]

        resource_id = self.resource_id = self.resource_id + 1

        resource_name = f'image_{resource_id}'

        dest_path = os.path.join(self.resources_dir, f'{resource_name}.{suffix}')

        if is_online:
            # Online
            print(f'Download: {url}; Suffix:{suffix}')
            wget.download(url, dest_path)

            if suffix == 'svg':
                from cairosvg import svg2png
                suffix = 'png'
                new_dest_path = os.path.join(self.resources_dir,
                                             f'{resource_name}.{suffix}')
                svg2png(url=dest_path, write_to=new_dest_path)
                os.remove(dest_path)
        else:
            shutil.copy(url, dest_path)

        block.attrib['image_idref'] = resource_name

        resource_element = et.SubElement(self.resources, 'resource')
        resource_element.attrib['id'] = resource_name
        resource_element.attrib['href'] = os.path.join('resources',
                                                       f'{resource_name}.{suffix}')

        return

    # Table
    def begin_table_block_context(self, context: TableBlockContext, **kwargs):
        block = self._create_block(context)
        self.current_page_block = block

    def begin_table_column_break_context(self, context: TableColumnBreakContext,
                                         **kwargs):
        element = self._create_element(context)

    def begin_table_row_break_context(self, context: TableRowBreakContext,
                                      **kwargs):
        element = self._create_element(context)

    # Audio
    def begin_audio_context(self, context: AudioTextContext,
                            **kwargs):
        block = self._create_element(context)

        url_pattern = r'^[a-z]*://'
        is_online = re.match(url_pattern, context.url)

        url = context.url

        if url.startswith('./'):
            url = url[2:]

        if self.current_file_path and not is_online:
            base_url = os.path.dirname(self.current_file_path)
            url = os.path.join(base_url, url)

        suffix = pathlib.Path(url).suffix[1:]

        resource_id = self.resource_id = self.resource_id + 1

        resource_name = f'audio_{resource_id}'

        dest_path = os.path.join(self.resources_dir, f'{resource_name}.{suffix}')

        if is_online:
            # Online
            print(f'Download: {url}; Suffix:{suffix}')
            wget.download(url, dest_path)
        else:
            shutil.copy(url, dest_path)

        block.attrib['audio_idref'] = resource_name

        resource_element = et.SubElement(self.resources, 'resource')
        resource_element.attrib['id'] = resource_name
        resource_element.attrib['href'] = os.path.join('resources',
                                                       f'{resource_name}.{suffix}')

        return
