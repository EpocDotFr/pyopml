from email.utils import format_datetime as datetime_to_rfc2822, parsedate_to_datetime as rfc2822_to_datetime
from .outlinable import Outlinable
from lxml import etree


class OpmlDocument(Outlinable):
    """Class that holds an OPML 2.0 document.

    :param str title: Title of the document
    :ivar title: Title of the document
    :vartype title: str

    :param datetime.datetime date_created: When the document was created
    :ivar date_created: When the document was created
    :vartype date_created: datetime.datetime

    :param datetime.datetime date_modified: When the document was last modified
    :ivar date_modified: When the document was last modified
    :vartype date_modified: datetime.datetime

    :param str owner_name: Owner of the document
    :ivar owner_name: Owner of the document
    :vartype owner_name: str

    :param str owner_email: Email address of the owner of the document
    :ivar owner_email: Email address of the owner of the document
    :vartype owner_email: str

    :param str owner_id: Unique URL that contains information that allows a human reader to communicate with the author of the document via email or other means. It also may be used to identify the author
    :ivar owner_id: Unique URL that contains information that allows a human reader to communicate with the author of the document via email or other means. It also may be used to identify the author
    :vartype owner_id: str

    :param list expansion_state: List of line numbers that are expanded. The line numbers in the list tell you which headlines to expand. The order is important. For each element in the list, X, starting at the first summit, navigate flatdown X times and expand. Repeat for each element in the list
    :ivar expansion_state: List of line numbers that are expanded. The line numbers in the list tell you which headlines to expand. The order is important. For each element in the list, X, starting at the first summit, navigate flatdown X times and expand. Repeat for each element in the list
    :vartype expansion_state: list

    :param int vert_scroll_state: Which line of the outline is displayed on the top line of the window. This number is calculated with the expansion state already applied
    :ivar vert_scroll_state: Which line of the outline is displayed on the top line of the window. This number is calculated with the expansion state already applied
    :vartype vert_scroll_state: int

    :param int window_top: Pixel location of the top edge of the window
    :ivar window_top: Pixel location of the top edge of the window
    :vartype window_top: int

    :param int window_left: Pixel location of the left edge of the window
    :ivar window_left: Pixel location of the left edge of the window
    :vartype window_left: int

    :param int window_bottom: Pixel location of the bottom edge of the window
    :ivar window_bottom: Pixel location of the bottom edge of the window
    :vartype window_bottom: int

    :param int window_right: Pixel location of the right edge of the window
    :ivar window_right: Pixel location of the right edge of the window
    :vartype window_right: int
    """
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

    def dumps(self, pretty=False, encoding='UTF-8'):
        """Serialize this document to a string.

        :raises ValueError:
        :param bool pretty: Whether to pretty print the outputted XML code or not
        :param str encoding: The encoding to use. Will also define the XML's encoding declaration
        :rtype: str
        """
        return etree.tostring(
            self.build_tree(),
            pretty_print=pretty,
            encoding=encoding,
            xml_declaration=True
        ).decode(encoding)

    def dump(self, fp, pretty=False, encoding='UTF-8'):
        """Serialize this document to a filename or file-like object.

        :raises ValueError:
        :param fp: A filename or file-like object
        :param bool pretty: Whether to pretty print the outputted XML code or not
        :param str encoding: The encoding to use. Will also define the XML's encoding declaration
        """
        etree.ElementTree(self.build_tree()).write(
            fp,
            pretty_print=pretty,
            encoding=encoding,
            xml_declaration=True
        )

    @classmethod
    def loads(cls, s):
        """Unserialize OPML 2.0 data from a string.

        :raises ValueError:
        :param str s: The string to unserialize from
        :rtype: opml.OpmlDocument
        """
        return cls.unbuild_tree(
            etree.fromstring(s)
        )

    @classmethod
    def load(cls, fp):
        """Unserialize OPML 2.0 data from a filename or file-like object.

        :raises ValueError:
        :param fp: A filename or file-like object
        :rtype: opml.OpmlDocument
        """
        return cls.unbuild_tree(
            etree.parse(fp).getroot()
        )

    @classmethod
    def unbuild_tree(cls, root):
        version = root.get('version')

        if not version:
            raise ValueError('"version" attribute not found in root node')
        elif version != '2.0':
            raise ValueError('This package only supports OPML 2.0 specification')

        document = cls()

        head = root.find('head')

        if head is None:
            raise ValueError('"head" node not found')

        title = head.findtext('title')

        if title:
            document.title = title

        date_created = head.findtext('dateCreated')

        if date_created:
            document.date_created = rfc2822_to_datetime(date_created)

        date_modified = head.findtext('dateModified')

        if date_modified:
            document.date_modified = rfc2822_to_datetime(date_modified)

        owner_name = head.findtext('ownerName')

        if owner_name:
            document.owner_name = owner_name

        owner_email = head.findtext('ownerEmail')

        if owner_email:
            document.owner_email = owner_email

        owner_id = head.findtext('ownerId')

        if owner_id:
            document.owner_id = owner_id

        expansion_state = head.findtext('expansionState')

        if expansion_state:
            document.expansion_state = expansion_state.split(',')

        vert_scroll_state = head.findtext('vertScrollState')

        if vert_scroll_state:
            document.vert_scroll_state = vert_scroll_state

        window_top = head.findtext('windowTop')

        if window_top:
            document.window_top = window_top

        window_left = head.findtext('windowLeft')

        if window_left:
            document.window_left = window_left

        window_bottom = head.findtext('windowBottom')

        if window_bottom:
            document.window_bottom = window_bottom

        window_right = head.findtext('windowRight')

        if window_right:
            document.window_right = window_right

        body = root.find('body')

        if body is None:
            raise ValueError('"body" node not found')

        document.unbuild_outlines_tree(body)

        return document

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

        etree.SubElement(head, 'docs').text = 'http://opml.org/spec2.opml'

        self.build_outlines_tree(body)

        return root
