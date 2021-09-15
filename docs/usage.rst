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

Continue reading to learn about what you can do.

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

* :func:`opml.OpmlDocument.add_rss` which adds an URL to a RSS feed:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

    document.add_rss(
        'Intelligence News Feed',
        'https://hendley-associates.com/feeds/intelligence.rss',
        version='RSS2',
        created=datetime.now()
    )

* :func:`opml.OpmlDocument.add_link` which adds an URL:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

    document.add_link(
        'Jack Ryan re-elected for second mandate',
        'https://hendley-associates.com/articles/usa/2021/08/02/jack-ryan-re-elected-second-mandate.html',
        language='en'
    )

* :func:`opml.OpmlDocument.add_include` which points to another OPML 2.0 file:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

    document.add_include(
        'All Feeds',
        'https://hendley-associates.com/feeds.opml',
        categories=['/Intelligence/USA', 'intelligence']
    )

* :func:`opml.OpmlDocument.add_outline`, a low-level method used by all the aforementioned ones, which can add any outline:

.. code-block:: python

    from opml import OpmlDocument

    document = OpmlDocument()

    document.add_outline('Codename: The Campus')

Creating outlines trees
***********************

The aforementioned methods all returns references to :class:`opml.OpmlOutline` instances that have just been created. This allows us to append outlines to others:

.. todo::

    Document.

Serializing OPML documents
--------------------------

.. todo::

    Document.

Unserializing OPML documents
----------------------------

.. todo::

    Document.

Full examples
-----------------

Here's Python implementations of examples as shown on the `official OPML site <http://opml.org/spec2.opml#1629043023000>`__:

* http://hosting.opml.org/dave/spec/subscriptionList.opml

.. toggle::

    .. include:: examples/subscription_list.py
        :code: python