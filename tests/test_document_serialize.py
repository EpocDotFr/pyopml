from email.utils import parsedate_to_datetime as rfc2822_to_datetime
from opml.exceptions import OpmlWriteError
from opml import OpmlDocument
import pytest
import re


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


def run_write_error_suite(document, tmp_path, error_message):
    filename = str(tmp_path / 'test.opml')

    with pytest.raises(OpmlWriteError, match=error_message):
        document.dumps(pretty=True)

    with pytest.raises(OpmlWriteError, match=error_message):
        document.dump(filename, pretty=True)

    with pytest.raises(OpmlWriteError, match=error_message):
        with open(filename, 'wb') as f:
            document.dump(f, pretty=True)


def test_missing_outline_text_attribute(document_with_rss_outline, tmp_path):
    document_with_rss_outline.outlines[0].outlines[0].text = None

    run_write_error_suite(
        document_with_rss_outline,
        tmp_path,
        'Required outline attribute "text" not found'
    )


def test_rss_outline_missing_xml_url(document_with_rss_outline, tmp_path):
    document_with_rss_outline.outlines[0].outlines[0].xml_url = None

    run_write_error_suite(
        document_with_rss_outline,
        tmp_path,
        re.escape('"xml_url" attribute is required for outlines of type "rss" (outline: "CIA News Feed")')
    )


def test_rss_outline_invalid_version(document_with_rss_outline, tmp_path):
    document_with_rss_outline.outlines[0].outlines[0].version = 'NONE'

    run_write_error_suite(
        document_with_rss_outline,
        tmp_path,
        re.escape('"version" attribute must be one of "RSS", "RSS1", "RSS2" or "scriptingNews" if set for outlines of type "rss" (outline: "CIA News Feed")')
    )


def test_link_outline_missing_url(document_with_link_outline, tmp_path):
    document_with_link_outline.outlines[0].outlines[0].url = None

    run_write_error_suite(
        document_with_link_outline,
        tmp_path,
        re.escape('"url" attribute is required for outlines of type "link" and "include" (outline: "Jack Ryan re-elected for second mandate")')
    )


def test_include_outline_missing_url(document_with_include_outline, tmp_path):
    document_with_include_outline.outlines[0].outlines[0].url = None

    run_write_error_suite(
        document_with_include_outline,
        tmp_path,
        re.escape('"url" attribute is required for outlines of type "link" and "include" (outline: "All Feeds")')
    )


def test_ok(document_with_everything, tmp_path):
    with open('tests/fixtures/valid.opml', 'r') as f:
        valid_opml_document_as_string = f.read()

    filename = str(tmp_path / 'test.opml')

    assert document_with_everything.dumps(pretty=True) == valid_opml_document_as_string

    document_with_everything.dump(filename, pretty=True)

    with open(filename, 'r') as f:
        target_opml_document_as_string = f.read()

    assert target_opml_document_as_string == valid_opml_document_as_string

    with open(filename, 'wb') as f:
        document_with_everything.dump(f, pretty=True)

    with open(filename, 'r') as f:
        target_opml_document_as_string = f.read()

    assert target_opml_document_as_string == valid_opml_document_as_string
