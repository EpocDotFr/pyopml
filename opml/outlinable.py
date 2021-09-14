class Outlinable:
    def __init__(self):
        self.outlines = []

    def add_outline(self, text, **kvargs):
        from .outline import OpmlOutline

        outline = OpmlOutline(text, **kvargs)

        self.outlines.append(outline)

        return outline

    def add_rss(self, text, xml_url, **kvargs):
        return self.add_outline(
            text,
            type='rss',
            xml_url=xml_url,
            **kvargs
        )

    def add_link(self, text, url, **kvargs):
        return self.add_outline(
            text,
            type='link',
            url=url,
            **kvargs
        )

    def add_include(self, text, url, **kvargs):
        return self.add_outline(
            text,
            type='include',
            url=url,
            **kvargs
        )

    def build_outlines_tree(self, parent):
        for outline in self.outlines:
            parent.append(outline.build_tree())
