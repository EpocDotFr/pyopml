from email.utils import format_datetime as datetime_to_rfc2822, parsedate_to_datetime as rfc2822_to_datetime
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

    def dumps(self, pretty=False, encoding='UTF-8', xml_declaration=True):
        return etree.tostring(
            self.build_tree(),
            pretty_print=pretty,
            encoding=encoding,
            xml_declaration=xml_declaration
        )

    def dump(self, fp, pretty=False, encoding='UTF-8', xml_declaration=True):
        etree.ElementTree(self.build_tree()).write(
            fp,
            pretty_print=pretty,
            encoding=encoding,
            xml_declaration=xml_declaration
        )

    def loads(self, s):
        self.unbuild_tree(
            etree.fromstring(s)
        )

    def load(self, fp):
        self.unbuild_tree(
            etree.parse(fp).getroot()
        )

    def unbuild_tree(self, root):
        version = root.get('version')

        if not version:
            raise ValueError('"version" attribute not found in root node')
        elif version != '2.0':
            raise ValueError('This package only supports OPML 2.0 specification')

        head = root.find('head')

        if not head:
            raise ValueError('"head" node not found')

        title = head.findtext('title')

        if title:
            self.title = title

        date_created = head.findtext('dateCreated')

        if date_created:
            self.date_created = rfc2822_to_datetime(date_created)

        date_modified = head.findtext('dateModified')

        if date_modified:
            self.date_modified = rfc2822_to_datetime(date_modified)

        owner_name = head.findtext('ownerName')

        if owner_name:
            self.owner_name = owner_name

        owner_email = head.findtext('ownerEmail')

        if owner_email:
            self.owner_email = owner_email

        owner_id = head.findtext('ownerId')

        if owner_id:
            self.owner_id = owner_id

        expansion_state = head.findtext('expansionState')

        if expansion_state:
            self.expansion_state = expansion_state.split(',')

        vert_scroll_state = head.findtext('vertScrollState')

        if vert_scroll_state:
            self.vert_scroll_state = vert_scroll_state

        window_top = head.findtext('windowTop')

        if window_top:
            self.window_top = window_top

        window_left = head.findtext('windowLeft')

        if window_left:
            self.window_left = window_left

        window_bottom = head.findtext('windowBottom')

        if window_bottom:
            self.window_bottom = window_bottom

        window_right = head.findtext('windowRight')

        if window_right:
            self.window_right = window_right

    def build_tree(self):
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
