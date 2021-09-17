from opml.exceptions import OpmlReadError
from opml import OpmlDocument
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

    assert isinstance(OpmlDocument.loads(file_as_string), OpmlDocument)

    assert isinstance(OpmlDocument.load(filename), OpmlDocument)

    with open(filename, 'r') as f:
        assert isinstance(OpmlDocument.load(f), OpmlDocument)
