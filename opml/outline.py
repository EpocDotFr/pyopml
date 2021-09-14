from email.utils import format_datetime as datetime_to_rfc2822, parsedate_to_datetime as rfc2822_to_datetime
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

    @classmethod
    def unbuild_tree(cls, node):
        text = node.get('text')

        if not text:
            raise ValueError('Required outline attribute "text" not found')

        outline = cls(text)

        type = node.get('type')

        if type:
            outline.type = type

        is_comment = node.get('isComment', 'false')

        if is_comment == 'true':
            outline.is_comment = True

        is_breakpoint = node.get('isBreakpoint', 'false')

        if is_breakpoint == 'true':
            outline.is_breakpoint = True

        created = node.get('created')

        if created:
            outline.created = rfc2822_to_datetime(created)

        xml_url = node.get('xmlUrl')

        if xml_url:
            outline.xml_url = xml_url

        description = node.get('description')

        if description:
            outline.description = description

        html_url = node.get('htmlUrl')

        if html_url:
            outline.html_url = html_url

        language = node.get('language')

        if language:
            outline.language = language

        title = node.get('title')

        if title:
            outline.title = title

        version = node.get('version')

        if version:
            outline.version = version

        url = node.get('url')

        if url:
            outline.url = url

        categories = node.get('category')

        if categories:
            outline.categories = categories.split(',')

        outline.unbuild_outlines_tree(node)

        return outline

    def build_tree(self):
        if not self.text:
            raise ValueError('"text" attribute is required for all outlines')

        node = etree.Element('outline', text=self.text)

        if self.type:
            if self.type == 'rss':
                if not self.xml_url:
                    raise ValueError('"xml_url" attribute is required for outlines of type "rss"')

                if self.version and self.version not in ('RSS', 'RSS1', 'RSS2', 'scriptingNews'):
                    raise ValueError('"version" attribute must be one of "RSS", "RSS1", "RSS2" or "scriptingNews" if set for outlines of type "rss"')
            elif self.type in ('link', 'include') and not self.url:
                raise ValueError('"url" attribute is required for outlines of type "link" and "include"')

            node.set('type', self.type)

        if self.is_comment:
            node.set('isComment', 'true')

        if self.is_breakpoint:
            node.set('isBreakpoint', 'true')

        if self.created:
            node.set('created', datetime_to_rfc2822(self.created))

        if self.xml_url:
            node.set('xmlUrl', self.xml_url)

        if self.description:
            node.set('description', self.description)

        if self.html_url:
            node.set('htmlUrl', self.html_url)

        if self.language:
            node.set('language', self.language)

        if self.title:
            node.set('title', self.title)

        if self.version:
            node.set('version', self.version)

        if self.url:
            node.set('url', self.url)

        if self.categories:
            node.set('category', ','.join(self.categories))

        self.build_outlines_tree(node)

        return node
