PyOPML documentation
====================

Welcome! This documentation is about PyOPML, a Python package meant to read, manipulate and write `OPML 2.0 <http://opml.org/spec2.opml>`__ files.

|pyversion| |pypiv| |pypil|

Prerequisites
-------------

  - Python 3.6+

Installation
------------

The usual way:

.. code-block:: console

    $ pip install pyopml

The McGyver way, after cloning/downloading this repo:

.. code-block:: console

    $ python setup.py install

Usage
-----

Creating OPML documents
***********************

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

Manipulating OPML documents
***************************

It's once you got an :class:`opml.OpmlDocument` instance that things starts to be interesting.

You can **get and set the document's metadata** using the aforementioned class' attributes:

.. code-block:: python

    from opml import OpmlDocument
    from datetime import datetime

    document = OpmlDocument()

    print(document.date_created) # None

    document.date_created = datetime.now()
    document.title = 'Hendley Associates - Feeds'

    print(document.date_created) # 2021-09-14 23:02:52.237540
    print(document.title) # Hendley Associates - Feeds

You can of course **add outlines** using :func:`opml.OpmlDocument.add_rss`, :func:`opml.OpmlDocument.add_link`, :func:`opml.OpmlDocument.add_include` and :func:`opml.OpmlDocument.add_outline`:

.. code-block:: python

    from opml import OpmlDocument
    from datetime import datetime

    document = OpmlDocument(title='Hendley Associates')

    # RSS
    document.add_rss(
        'Intelligence News Feed',
        'https://hendley-associates.com/feeds/intelligence.rss',
        version='RSS2',
        created=datetime.now()
    )

    # Link
    document.add_link(
        'Jack Ryan re-elected for second mandate',
        'https://hendley-associates.com/articles/usa/2021/08/02/jack-ryan-re-elected-second-mandate.html',
        language='en'
    )

    # Include
    document.add_include(
        'All Feeds',
        'https://hendley-associates.com/feeds.opml',
        categories=['/Intelligence/USA', 'intelligence']
    )

    # Custom (used internally but of course publicly available)
    document.add_outline('I am just a label')

Serializing OPML documents
**************************

.. todo::

    Document.

Unserializing OPML documents
****************************

.. todo::

    Document.

API docs
--------

.. autoclass:: opml.OpmlDocument
   :members:

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/pyopml.svg?link=https://pypi.python.org/pypi/pyopml
.. |pypiv| image:: https://img.shields.io/pypi/v/pyopml.svg?link=https://pypi.python.org/pypi/pyopml
.. |pypil| image:: https://img.shields.io/pypi/l/pyopml.svg?link=https://github.com/EpocDotFr/pyopml/blob/master/LICENSE.md