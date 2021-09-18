from email.utils import parsedate_to_datetime as rfc2822_to_datetime
from opml import OpmlDocument
import pytest


def add_rss_fixture(document):
    feeds = document.add_outline('Feeds')

    feeds.add_rss(
        'CIA News Feed',
        'https://hendley-associates.com/feeds/cia.rss',
        description='CIA News Feed',
        html_url='https://hendley-associates.com/news/cia',
        language='en_US',
        title='CIA News Feed',
        version='RSS2',
        created=rfc2822_to_datetime('Thu, 16 Sep 2021 20:07:59 -0000'),
        categories=['/Intelligence/USA', 'intelligence']
    )

    return document


def add_link_fixture(document):
    links = document.add_outline('Links')

    links.add_link(
        'Jack Ryan re-elected for second mandate',
        'https://hendley-associates.com/articles/usa/2021/08/02/jack-ryan-re-elected-second-mandate.html',
        created=rfc2822_to_datetime('Thu, 16 Sep 2021 20:07:59 -0000'),
        categories=['/Intelligence/USA', 'intelligence']
    )

    return document


def add_include_fixture(document):
    includes = document.add_outline('Includes')

    includes.add_include(
        'All Feeds',
        'https://hendley-associates.com/feeds.opml',
        created=rfc2822_to_datetime('Thu, 16 Sep 2021 20:07:59 -0000'),
        categories=['/Intelligence/USA', 'intelligence']
    )

    return document


@pytest.fixture
def document():
    document = OpmlDocument()
    document.title = 'Hendley Associates Feed'
    document.date_created = rfc2822_to_datetime('Thu, 16 Sep 2021 20:07:59 -0000')
    document.date_modified = rfc2822_to_datetime('Thu, 16 Sep 2021 20:07:59 -0000')
    document.owner_name = 'Gerry Hendley'
    document.owner_email = 'gerry@hendley-associates.com'
    document.owner_id = 'https://hendley-associates.com'
    document.expansion_state = [2, 5]
    document.vert_scroll_state = 4
    document.window_top = 50
    document.window_left = 50
    document.window_bottom = 50
    document.window_right = 50

    return document


@pytest.fixture
def document_with_rss_outline(document):
    return add_rss_fixture(document)


@pytest.fixture
def document_with_link_outline(document):
    return add_link_fixture(document)


@pytest.fixture
def document_with_include_outline(document):
    return add_include_fixture(document)


@pytest.fixture
def document_with_everything(document):
    add_rss_fixture(document)
    add_link_fixture(document)
    add_include_fixture(document)

    return document
