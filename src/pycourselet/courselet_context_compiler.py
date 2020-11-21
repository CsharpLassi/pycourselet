import os
import shutil
import tempfile
import xml.etree.ElementTree as et
from typing import Optional

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
            SubHeadingContext: (
                self.begin_sub_heading_context,
                self.end_sub_heading_context),
            SubHeadingTextContext: (
                self.begin_sub_heading_text_context,
                self.end_sub_heading_text_context),
            ParagraphContext: (
                self.begin_paragraph_context,
                self.end_paragraph_context),
        }

        context_type = type(context)

        if context_type in methods:
            methods[context_type][0](context, **kwargs)

        for child in context.children:
            self._listen_context(child, ctx, **kwargs)

        if context_type in methods:
            methods[context_type][1](context, **kwargs)

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

    def begin_sub_heading_context(self, context: SubHeadingContext, **kwargs):
        return

    def end_sub_heading_context(self, context: SubHeadingContext, **kwargs):
        return

    def begin_sub_heading_text_context(self, context: SubHeadingTextContext,
                                       **kwargs):
        return

    def end_sub_heading_text_context(self, context: SubHeadingTextContext, **kwargs):
        return

    def begin_paragraph_context(self, context: ParagraphContext,
                                **kwargs):
        return

    def end_paragraph_context(self, context: SubHeadingTextContext, **kwargs):
        return


class CourseletXmlContextCompiler(CourseletContextCompiler):
    def __init__(self, name: str, output_file: str):
        self.name = name
        self.output_file = output_file

        self.build_dir = tempfile.TemporaryDirectory(prefix='pycourselet_').name
        self.page_dir = os.path.join(self.build_dir, 'pages')
        self.resources_dir = os.path.join(self.build_dir, 'resources')

        self.courselet_element: et.Element = et.Element('courselet')
        self.meta: et.Element = et.SubElement(self.courselet_element, 'meta')
        self.pages: et.Element = et.SubElement(self.courselet_element, 'pages')

        self.current_page: Optional[et.Element] = None
        self.current_page_content: Optional[et.Element] = None

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

    def end_page_context(self, context: PageContext, **kwargs):
        root = et.ElementTree(self.current_page)
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

    # Heading
    def begin_heading_context(self, context: HeadingContext, **kwargs):
        block = self._create_block(context)
        self.current_page_block = block

    def begin_heading_text_context(self, context: HeadingTextContext,
                                   **kwargs):
        element = self._create_element(context)
        element.text = context.text

    # Sub Heading
    def begin_sub_heading_context(self, context: SubHeadingContext, **kwargs):
        block = self._create_block(context)
        self.current_page_block = block

    def begin_sub_heading_text_context(self, context: SubHeadingTextContext,
                                       **kwargs):
        element = self._create_element(context)
        element.text = context.text
