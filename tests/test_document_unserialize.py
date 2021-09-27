from opml import OpmlDocument, OpmlOutline
from opml.exceptions import OpmlReadError
from datetime import datetime
import pytest
import re


def run_read_error_suite(filename, error_message):
    with open(filename, 'r') as f:
        file_as_string = f.read()

    with pytest.raises(OpmlReadError, match=error_message):
        OpmlDocument.loads(file_as_string)

    with pytest.raises(OpmlReadError, match=error_message):
        OpmlDocument.load(filename)

    with pytest.raises(OpmlReadError, match=error_message):
        with open(filename, 'r') as f:
            OpmlDocument.load(f)


def validate_valid_opml_document(document):
    assert isinstance(document, OpmlDocument)
    assert document.title == 'Hendley Associates Feed'
    assert isinstance(document.date_created, datetime)
    assert isinstance(document.date_modified, datetime)
    assert document.owner_name == 'Gerry Hendley'
    assert document.owner_email == 'gerry@hendley-associates.com'
    assert document.owner_id == 'https://hendley-associates.com'
    assert document.expansion_state == ['2', '5']
    assert document.vert_scroll_state == '4'
    assert document.window_top == '50'
    assert document.window_left == '50'
    assert document.window_bottom == '50'
    assert document.window_right == '50'

    assert len(document.outlines) == 3

    # Feeds

    feeds_outline = document.outlines[0]

    assert isinstance(feeds_outline, OpmlOutline)
    assert feeds_outline.text == 'Feeds'

    assert len(feeds_outline.outlines) == 1

    rss_outline = feeds_outline.outlines[0]

    assert isinstance(rss_outline, OpmlOutline)
    assert rss_outline.text == 'CIA News Feed'
    assert rss_outline.type == 'rss'
    assert isinstance(rss_outline.created, datetime)
    assert rss_outline.xml_url == 'https://hendley-associates.com/feeds/cia.rss'
    assert rss_outline.description == 'CIA News Feed'
    assert rss_outline.html_url == 'https://hendley-associates.com/news/cia'
    assert rss_outline.language == 'en_US'
    assert rss_outline.title == 'CIA News Feed'
    assert rss_outline.version == 'RSS2'
    assert rss_outline.categories == ['/Intelligence/USA', 'intelligence']

    # Links

    links_outline = document.outlines[1]

    assert isinstance(links_outline, OpmlOutline)
    assert links_outline.text == 'Links'

    assert len(links_outline.outlines) == 1

    link_outline = links_outline.outlines[0]

    assert isinstance(link_outline, OpmlOutline)
    assert link_outline.text == 'Jack Ryan re-elected for second mandate'
    assert link_outline.type == 'link'
    assert isinstance(link_outline.created, datetime)
    assert link_outline.url == 'https://hendley-associates.com/articles/usa/2021/08/02/jack-ryan-re-elected-second-mandate.html'
    assert link_outline.categories == ['/Intelligence/USA', 'intelligence']

    # Includes

    includes_outline = document.outlines[2]

    assert isinstance(includes_outline, OpmlOutline)
    assert includes_outline.text == 'Includes'

    assert len(includes_outline.outlines) == 1

    include_outline = includes_outline.outlines[0]

    assert isinstance(include_outline, OpmlOutline)
    assert include_outline.text == 'All Feeds'
    assert include_outline.type == 'include'
    assert isinstance(include_outline.created, datetime)
    assert include_outline.url == 'https://hendley-associates.com/feeds.opml'
    assert include_outline.categories == ['/Intelligence/USA', 'intelligence']


def test_not_an_opml_document():
    run_read_error_suite(
        'tests/fixtures/not_an_opml_document.xml',
        'Not an OPML document'
    )


def test_no_version():
    run_read_error_suite(
        'tests/fixtures/no_version.opml',
        '"version" attribute not found in root node'
    )


def test_unsupported_version():
    run_read_error_suite(
        'tests/fixtures/unsupported_version.opml',
        'This package only supports OPML 2.0 specification'
    )


def test_no_head():
    run_read_error_suite(
        'tests/fixtures/no_head.opml',
        '"head" node not found'
    )


def test_no_body():
    run_read_error_suite(
        'tests/fixtures/no_body.opml',
        '"body" node not found'
    )


def test_missing_outline_text_attribute():
    run_read_error_suite(
        'tests/fixtures/missing_outline_text_attribute.opml',
        'Required outline attribute "text" not found'
    )


def test_rss_outline_missing_xml_url():
    run_read_error_suite(
        'tests/fixtures/rss_outline_missing_xml_url.opml',
        re.escape('"xml_url" attribute is required for outlines of type "rss" (outline: "CIA News Feed")')
    )


def test_rss_outline_invalid_version():
    run_read_error_suite(
        'tests/fixtures/rss_outline_invalid_version.opml',
        re.escape('"version" attribute must be one of "RSS", "RSS1", "RSS2" or "scriptingNews" if set for outlines of type "rss" (outline: "CIA News Feed")')
    )


def test_link_outline_missing_url():
    run_read_error_suite(
        'tests/fixtures/link_outline_missing_url.opml',
        re.escape('"url" attribute is required for outlines of type "link" and "include" (outline: "Jack Ryan re-elected for second mandate")')
    )


def test_include_outline_missing_url():
    run_read_error_suite(
        'tests/fixtures/include_outline_missing_url.opml',
        re.escape('"url" attribute is required for outlines of type "link" and "include" (outline: "All Feeds")')
    )


def test_valid():
    filename = 'tests/fixtures/valid.opml'

    with open(filename, 'r') as f:
        file_as_string = f.read()

    validate_valid_opml_document(OpmlDocument.loads(file_as_string))

    validate_valid_opml_document(OpmlDocument.load(filename))

    with open(filename, 'r') as f:
        validate_valid_opml_document(OpmlDocument.load(f))
