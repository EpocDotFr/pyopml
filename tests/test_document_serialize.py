from opml.exceptions import OpmlWriteError
import pytest
import re


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
