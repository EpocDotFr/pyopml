from email.utils import format_datetime as datetime_to_rfc2822
from .outlinable import Outlinable
from lxml import etree


class OpmlDocument(Outlinable):
    def __init__(self, **kvargs):
        super(OpmlDocument, self).__init__()

        self.title = kvargs.get('title')
        self.date_created = kvargs.get('date_created')
        self.date_modified = kvargs.get('date_modified')
        self.owner_name = kvargs.get('owner_name')
        self.owner_email = kvargs.get('owner_email')
        self.owner_id = kvargs.get('owner_id')
        self.expansion_state = kvargs.get('expansion_state', [])
        self.vert_scroll_state = kvargs.get('vert_scroll_state')
        self.window_top = kvargs.get('window_top')
        self.window_left = kvargs.get('window_left')
        self.window_bottom = kvargs.get('window_bottom')
        self.window_right = kvargs.get('window_right')

    def to_string(self, pretty=False, encoding='UTF-8', xml_declaration=True):
        return etree.tostring(
            self._build_tree(),
            pretty_print=pretty,
            encoding=encoding,
            xml_declaration=xml_declaration
        )

    def to_file(self, file_or_filename, pretty=False, encoding='UTF-8', xml_declaration=True):
        etree.ElementTree(self._build_tree()).write(
            file_or_filename,
            pretty_print=pretty,
            encoding=encoding,
            xml_declaration=xml_declaration
        )

    def _build_tree(self):
        root = etree.Element('opml', version='2.0')
        head = etree.SubElement(root, 'head')
        body = etree.SubElement(root, 'body')

        if self.title:
            etree.SubElement(head, 'title').text = self.title

        if self.date_created:
            etree.SubElement(head, 'dateCreated').text = datetime_to_rfc2822(self.date_created)

        if self.date_modified:
            etree.SubElement(head, 'dateModified').text = datetime_to_rfc2822(self.date_modified)

        if self.owner_name:
            etree.SubElement(head, 'ownerName').text = self.owner_name

        if self.owner_email:
            etree.SubElement(head, 'ownerEmail').text = self.owner_email

        if self.owner_id:
            etree.SubElement(head, 'ownerId').text = self.owner_id

        if self.expansion_state:
            etree.SubElement(head, 'expansionState').text = ','.join(self.expansion_state)

        if self.vert_scroll_state:
            etree.SubElement(head, 'vertScrollState').text = self.vert_scroll_state

        if self.window_top:
            etree.SubElement(head, 'windowTop').text = self.window_top

        if self.window_left:
            etree.SubElement(head, 'windowLeft').text = self.window_left

        if self.window_bottom:
            etree.SubElement(head, 'windowBottom').text = self.window_bottom

        if self.window_right:
            etree.SubElement(head, 'windowRight').text = self.window_right

        etree.SubElement(head, 'docs').text = 'http://dev.opml.org/spec2.html'

        self.build_outlines_tree(body)

        return root
