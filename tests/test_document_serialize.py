from opml.exceptions import OpmlWriteError
from opml import OpmlDocument
from datetime import datetime
import pytest
import re


@pytest.fixture
def document():
    document = OpmlDocument()
    document.title = 'Hendley Associates Feed'
    document.date_created = datetime.now()
    document.date_modified = datetime.now()
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
    document.add_rss(
        'CIA News Feed',
        'https://hendley-associates.com/feeds/cia.rss',
        description='CIA News Feed',
        html_url='https://hendley-associates.com/news/cia',
        language='en_US',
        title='CIA News Feed',
        version='RSS2',
        created=datetime.now(),
        categories=['/Intelligence/USA', 'intelligence']
    )

    return document


@pytest.fixture
def document_with_link_outline(document):
    document.add_link(
        'Jack Ryan re-elected for second mandate',
        'https://hendley-associates.com/articles/usa/2021/08/02/jack-ryan-re-elected-second-mandate.html',
        created=datetime.now(),
        categories=['/Intelligence/USA', 'intelligence']
    )

    return document


@pytest.fixture
def document_with_include_outline(document):
    document.add_include(
        'All Feeds',
        'https://hendley-associates.com/feeds.opml',
        created=datetime.now(),
        categories=['/Intelligence/USA', 'intelligence']
    )

    return document


def run_write_error_suite(document, tmp_path, error_message):
    filename = str(tmp_path / 'test.opml')

    with pytest.raises(OpmlWriteError, match=error_message):
        document.dumps()

    with pytest.raises(OpmlWriteError, match=error_message):
        document.dump(filename)

    with pytest.raises(OpmlWriteError, match=error_message):
        with open(filename, 'w') as f:
            document.dump(f)


def test_missing_outline_text_attribute(document_with_rss_outline, tmp_path):
    document_with_rss_outline.outlines[0].text = None

    run_write_error_suite(
        document_with_rss_outline,
        tmp_path,
        'Required outline attribute "text" not found'
    )


def test_rss_outline_missing_xml_url(document_with_rss_outline, tmp_path):
    document_with_rss_outline.outlines[0].xml_url = None

    run_write_error_suite(
        document_with_rss_outline,
        tmp_path,
        re.escape('"xml_url" attribute is required for outlines of type "rss" (outline: "CIA News Feed")')
    )


def test_rss_outline_invalid_version(document_with_rss_outline, tmp_path):
    document_with_rss_outline.outlines[0].version = 'NONE'

    run_write_error_suite(
        document_with_rss_outline,
        tmp_path,
        re.escape('"version" attribute must be one of "RSS", "RSS1", "RSS2" or "scriptingNews" if set for outlines of type "rss" (outline: "CIA News Feed")')
    )


def test_link_outline_missing_url(document_with_link_outline, tmp_path):
    document_with_link_outline.outlines[0].url = None

    run_write_error_suite(
        document_with_link_outline,
        tmp_path,
        re.escape('"url" attribute is required for outlines of type "link" and "include" (outline: "Jack Ryan re-elected for second mandate")')
    )


def test_include_outline_missing_url(document_with_include_outline, tmp_path):
    document_with_include_outline.outlines[0].url = None

    run_write_error_suite(
        document_with_include_outline,
        tmp_path,
        re.escape('"url" attribute is required for outlines of type "link" and "include" (outline: "All Feeds")')
    )


def test_ok(document_with_rss_outline, tmp_path):
    filename = str(tmp_path / 'test.opml')

    assert isinstance(document_with_rss_outline.dumps(), str)

    document_with_rss_outline.dump(filename)

    with open(filename, 'w') as f:
        document_with_rss_outline.dump(f)
