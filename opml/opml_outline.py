from email.utils import format_datetime as datetime_to_rfc2822
from .outlinable import Outlinable
from lxml import etree


class OpmlOutline(Outlinable):
    def __init__(self, text, **kvargs):
        super(OpmlOutline, self).__init__()

        self.text = text
        self.type = kvargs.get('type')
        self.is_comment = kvargs.get('is_comment', False)
        self.is_breakpoint = kvargs.get('is_breakpoint', False)
        self.created = kvargs.get('created')
        self.xml_url = kvargs.get('xml_url')
        self.description = kvargs.get('description')
        self.html_url = kvargs.get('html_url')
        self.language = kvargs.get('language')
        self.title = kvargs.get('title')
        self.version = kvargs.get('version')
        self.url = kvargs.get('url')
        self.categories = kvargs.get('categories', [])

    def build_tree(self):
        if not self.text:
            raise ValueError('"text" attribute is required for all outlines')

        element = etree.Element('outline', text=self.text)

        if self.type:
            if self.type == 'rss':
                if not self.xml_url:
                    raise ValueError('"xml_url" attribute is required for outlines of type "rss"')

                if self.version and self.version not in ('RSS', 'RSS1', 'RSS2', 'scriptingNews'):
                    raise ValueError('"version" attribute must be one of "RSS", "RSS1", "RSS2" or "scriptingNews" if set for outlines of type "rss"')
            elif self.type in ('link', 'include') and not self.url:
                raise ValueError('"url" attribute is required for outlines of type "link" and "include"')

            element.set('type', self.type)

        if self.is_comment:
            element.set('isComment', 'true')

        if self.is_breakpoint:
            element.set('isBreakpoint', 'true')

        if self.created:
            element.set('created', datetime_to_rfc2822(self.created))

        if self.xml_url:
            element.set('xmlUrl', self.xml_url)

        if self.description:
            element.set('description', self.description)

        if self.html_url:
            element.set('htmlUrl', self.html_url)

        if self.language:
            element.set('language', self.language)

        if self.title:
            element.set('title', self.title)

        if self.version:
            element.set('version', self.version)

        if self.url:
            element.set('url', self.url)

        if self.categories:
            element.set('category', ','.join(self.categories))

        self.build_outlines_tree(element)

        return element
