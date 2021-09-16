class Outlinable:
    def __init__(self):
        self.outlines = []

    def add_outline(self, text, **kvargs):
        """Create a new outline, append it to this object's outlines and return it.

        :param str text: Text of the outline
        :param str type: How the other attributes of the outline are interpreted. One of ``rss``, ``link`` or ``include``
        :param bool is_comment: Whether the outline is commented or not
        :param bool is_breakpoint: Whether a breakpoint is set on this outline
        :param datetime.datetime created: Date-time that the outline node was created
        :param str xml_url: URL to the feed when ``type`` is ``rss``
        :param str description: Top-level description element from the feed (if this outline is part of a subscription list)
        :param str html_url: Top-level link element from the feed (if this outline is part of a subscription list)
        :param str language: Top-level language element from the feed (if this outline is part of a subscription list)
        :param str title: Top-level title element from the feed (if this outline is part of a subscription list)
        :param str version: RSS version when ``type`` is ``rss``. One of ``RSS``, ``RSS1``, ``RSS2`` or ``scriptingNews``
        :param str url: An URL to a web page when ``type`` is ``link``
        :param list categories: A list of `RSS 2.0 <https://validator.w3.org/feed/docs/rss2.html#ltcategorygtSubelementOfLtitemgt>`__ categories. To represent a "tag", the category string should contain no slashes
        :rtype: opml.OpmlOutline
        """
        from opml.outline import OpmlOutline

        outline = OpmlOutline(text, **kvargs)

        self.outlines.append(outline)

        return outline

    def add_rss(self, text, xml_url, description=None, html_url=None, language=None, title=None, version=None, is_comment=False, is_breakpoint=False, created=None, categories=[]):
        """Create a new outline of type "rss", append it to this object's outlines and return it.

        :param str text: Text of the outline
        :param str xml_url: URL to the feed
        :param str description: Top-level description element from the feed (if this outline is part of a subscription list)
        :param str html_url: Top-level link element from the feed (if this outline is part of a subscription list)
        :param str language: Top-level language element from the feed (if this outline is part of a subscription list)
        :param str title: Top-level title element from the feed (if this outline is part of a subscription list)
        :param str version: RSS version. One of ``RSS``, ``RSS1``, ``RSS2`` or ``scriptingNews``
        :param bool is_comment: Whether the outline is commented or not
        :param bool is_breakpoint: Whether a breakpoint is set on this outline
        :param datetime.datetime created: Date-time that the outline node was created
        :param list categories: A list of `RSS 2.0 <https://validator.w3.org/feed/docs/rss2.html#ltcategorygtSubelementOfLtitemgt>`__ categories. To represent a "tag", the category string should contain no slashes
        :rtype: opml.OpmlOutline
        """
        return self.add_outline(
            text,
            type='rss',
            xml_url=xml_url,
            description=description,
            html_url=html_url,
            language=language,
            title=title,
            version=version,
            is_comment=is_comment,
            is_breakpoint=is_breakpoint,
            created=created,
            categories=categories
        )

    def add_link(self, text, url, is_comment=False, is_breakpoint=False, created=None, categories=[]):
        """Create a new outline of type "link", append it to this object's outlines and return it.

        :param str text: Text of the outline
        :param str url: An URL to a web page
        :param bool is_comment: Whether the outline is commented or not
        :param bool is_breakpoint: Whether a breakpoint is set on this outline
        :param datetime.datetime created: Date-time that the outline node was created
        :param list categories: A list of `RSS 2.0 <https://validator.w3.org/feed/docs/rss2.html#ltcategorygtSubelementOfLtitemgt>`__ categories. To represent a "tag", the category string should contain no slashes
        :rtype: opml.OpmlOutline
        """
        return self.add_outline(
            text,
            type='link',
            url=url,
            is_comment=is_comment,
            is_breakpoint=is_breakpoint,
            created=created,
            categories=categories
        )

    def add_include(self, text, url, is_comment=False, is_breakpoint=False, created=None, categories=[]):
        """Create a new outline of type "include", append it to this object's outlines and return it.

        :param str text: Text of the outline
        :param str url: An URL to an OPML document
        :param bool is_comment: Whether the outline is commented or not
        :param bool is_breakpoint: Whether a breakpoint is set on this outline
        :param datetime.datetime created: Date-time that the outline node was created
        :param list categories: A list of `RSS 2.0 <https://validator.w3.org/feed/docs/rss2.html#ltcategorygtSubelementOfLtitemgt>`__ categories. To represent a "tag", the category string should contain no slashes
        :rtype: opml.OpmlOutline
        """
        return self.add_outline(
            text,
            type='include',
            url=url,
            is_comment=is_comment,
            is_breakpoint=is_breakpoint,
            created=created,
            categories=categories
        )

    def build_outlines_tree(self, parent):
        for outline in self.outlines:
            parent.append(outline.build_tree())

    def unbuild_outlines_tree(self, parent):
        from opml.outline import OpmlOutline

        for node in parent.iterchildren(tag='outline'):
            self.outlines.append(
                OpmlOutline.unbuild_tree(node)
            )
