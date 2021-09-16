from opml.exceptions import OpmlReadError
from opml import OpmlDocument
import pytest


def run_read_error_suite(filename, error_message):
    with open(filename, 'r') as f:
        file_as_string = '\n'.join(f.readlines()[1:])

    with pytest.raises(OpmlReadError, match=error_message):
        OpmlDocument.loads(file_as_string)

    with pytest.raises(OpmlReadError, match=error_message):
        OpmlDocument.load(filename)

    with pytest.raises(OpmlReadError, match=error_message):
        with open(filename, 'r') as f:
            OpmlDocument.load(f)


def test_not_an_opml_file():
    run_read_error_suite(
        'tests/fixtures/not_an_opml_file.xml',
        'Not an OPML document'
    )


def test_opml_file_no_version():
    run_read_error_suite(
        'tests/fixtures/opml_file_no_version.opml',
        '"version" attribute not found in root node'
    )


def test_opml_file_unsupported_version():
    run_read_error_suite(
        'tests/fixtures/opml_file_unsupported_version.opml',
        'This package only supports OPML 2.0 specification'
    )


def test_opml_file_no_head():
    run_read_error_suite(
        'tests/fixtures/opml_file_no_head.opml',
        '"head" node not found'
    )


def test_opml_file_no_body():
    run_read_error_suite(
        'tests/fixtures/opml_file_no_body.opml',
        '"body" node not found'
    )


def test_opml_file_valid():
    filename = 'tests/fixtures/opml_file_valid.opml'

    with open(filename, 'r') as f:
        file_as_string = '\n'.join(f.readlines()[1:])

    assert isinstance(OpmlDocument.loads(file_as_string), OpmlDocument)

    assert isinstance(OpmlDocument.load(filename), OpmlDocument)

    with open(filename, 'r') as f:
        assert isinstance(OpmlDocument.load(f), OpmlDocument)
