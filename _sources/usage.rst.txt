Usage
=====

Creating OPML documents
-----------------------

PyOPML allows you to create OPML 2.0 documents from scratch, which may or may not be :ref:`serialized <Serializing OPML documents>` to a file or as a string afterhand. It all starts by instantiating a new :class:`opml.OpmlDocument` object. None of the constructor's arguments are required, so you could just:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

Already knows some of the argument's values? Just pass them:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument(
        title='Hendley Associates',
        owner_name='Gerry Hendley',
        owner_email='gerry@hendley-associates.com'
    )

Unserializing OPML documents
----------------------------

You may not want to create OPML 2.0 documents from scratch. PyOPML allows to unserialize existing ones instead, by providing two class methods:

* :meth:`opml.OpmlDocument.load` which unserializes a document from a filename or a file-like object:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument.load('hendley_associates.opml')

    # Or:

    with open('hendley_associates.opml', 'r') as f:
        document = OpmlDocument.load(f)

* :meth:`opml.OpmlDocument.loads` which unserializes a document from a string:

.. code-block:: python

    from opml import OpmlDocument

    document_as_string = """<?xml version='1.0' encoding='UTF-8'?>
    <opml version="2.0">
      <head>
        <docs>http://opml.org/spec2.opml</docs>
      </head>
      <body>
        <outline text="Hendley Associates - External Operations" type="rss" xmlUrl="https://hendley-associates.com/feeds/extops.rss" language="en_US" version="RSS2" />
      </body>
    </opml>"""

    document = OpmlDocument.loads(document_as_string)

Manipulating OPML documents
---------------------------

It's once you got an :class:`opml.OpmlDocument` instance that things starts to be interesting.

Getting and setting document's metadata
***************************************

Use the :class:`opml.OpmlDocument` instance attributes, Luke:

.. code-block:: python

    from opml import OpmlDocument
    from datetime import datetime

    document = OpmlDocument()

    print(document.date_created) # None
    print(document.title) # None

    document.date_created = datetime.now()
    document.title = 'Hendley Associates - Feeds'

    print(document.date_created) # 2021-09-14 23:02:52.237540
    print(document.title) # Hendley Associates - Feeds

Adding outlines to the document
*******************************

There a bunch of methods for that:

* :meth:`opml.OpmlDocument.add_rss` which adds a RSS feed:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

    document.add_rss(
        'Intelligence News Feed',
        'https://hendley-associates.com/feeds/intelligence.rss',
        version='RSS2',
        created=datetime.now()
    )

* :meth:`opml.OpmlDocument.add_link` which adds an URL:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

    document.add_link(
        'Jack Ryan re-elected for second mandate',
        'https://hendley-associates.com/articles/usa/2021/08/02/jack-ryan-re-elected-second-mandate.html'
    )

* :meth:`opml.OpmlDocument.add_include` which points to another OPML 2.0 file:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

    document.add_include(
        'All Feeds',
        'https://hendley-associates.com/feeds.opml',
        categories=['/Intelligence/USA', 'intelligence']
    )

* :meth:`opml.OpmlDocument.add_outline`, a low-level method used by all the aforementioned ones:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

    document.add_outline('Intelligence Agencies Feeds')

Getting and setting outline's data
**********************************

The aforementioned methods all returns references to :class:`opml.OpmlOutline` instances that have just been created. Again, use the attributes, Luke:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

    feed = document.add_rss(
        'Hendley Associates - External Operations',
        'https://hendley-associates.com/feeds/extops.rss',
        version='RSS2',
        created=datetime.now()
    )

    print(feed.language) # None
    print(feed.categories) # []

    feed.language = 'en_US'
    feed.categories.append('/Hendley Associates/EXTOPS')

    print(feed.language) # en_US
    print(feed.categories) # ['/Hendley Associates/EXTOPS']

Creating outlines trees
***********************

:class:`opml.OpmlOutline` instances themselves shares the same aforementioned methods, which allows us to append outlines to another in a tree-like fashion:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

    campus = document.add_outline('The Campus')

    campus_active = campus.add_outline('Active Duty')

    campus_active.add_link(
        'John Clark',
        'https://jackryan.fandom.com/wiki/John_Clark'
    )

    campus_active.add_link(
        'Jack Ryan, Jr.',
        'https://jackryan.fandom.com/wiki/Jack_Ryan,_Jr.'
    )

    campus_kia = campus.add_outline('KIA')

    campus_kia.add_link(
        'Brian Caruso',
        'https://jackryan.fandom.com/wiki/Brian_Caruso'
    )

    campus_kia.add_link(
        'Sam Driscoll',
        'https://jackryan.fandom.com/wiki/Sam_Driscoll'
    )

Outlines may contain as many outlines as you'd like.

Serializing OPML documents
--------------------------

Finally, you'll want to save OPML 2.0 documents you created or manipulated. PyOPML provides two methods:

* :meth:`opml.OpmlDocument.dump` which serializes the document to a filename or a file-like object:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()
    document.title = 'Hendley Associates Feed'
    document.date_created = datetime.now()
    document.owner_id = 'https://hendley-associates.com'
    document.owner_name = 'Gerry Hendley'
    document.owner_email = 'gerry@hendley-associates.com'

    document.dump('hendley_associates.opml', pretty=True)

    # Or:

    # Notice the opening mode: write+binary. lxml (used internally) will
    # complain if you're opening the file in text mode.
    with open('hendley_associates.opml', 'wb') as f:
        document.dump(f, pretty=True)

* :meth:`opml.OpmlDocument.dumps` which serializes the document to a string:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()
    document.title = 'Hendley Associates Feed'
    document.date_created = datetime.now()
    document.owner_id = 'https://hendley-associates.com'
    document.owner_name = 'Gerry Hendley'
    document.owner_email = 'gerry@hendley-associates.com'

    print(document.dumps()) # <?xml version='1.0' encoding='UTF-8'?>\n<opml version="2.0">...

.. tip::

    :class:`opml.OpmlDocument` implements :py:meth:`object.__str__`, which have the same behavior as :meth:`opml.OpmlDocument.dumps` except the encoding is forced to UTF-8 and pretty-print is enabled by default.