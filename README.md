# PyOPML

Python package meant to read, manipulate and write [OPML 2.0](http://opml.org/spec2.opml) files.

![Python versions](https://img.shields.io/pypi/pyversions/pyopml.svg?link=https://pypi.python.org/pypi/pyopml) ![Version](https://img.shields.io/pypi/v/pyopml.svg?link=https://pypi.python.org/pypi/pyopml) ![License](https://img.shields.io/pypi/l/pyopml.svg?link=https://pypi.python.org/pypi/pyopml?link=https://github.com/EpocDotFr/pyopml/blob/master/LICENSE.md)

## Documentation

Everything you need to know is located [here](https://epocdotfr.github.io/pyopml/).

## Changelog

See [here](https://github.com/EpocDotFr/pyopml/releases).

## Development

**Getting source code, installing the package as well as its dev packages:**

  1. Clone the repository
  2. From its root directory, run: `pip install --editable .[dev]`

**Running tests:**

From the root directory, run `pytest`. They will automatically be all discovered and ran.

**Building docs:**

From the `docs` directory, run `make.bat html` on Windows or `make html` on Linux.

**Publishing the package:**

From the root directory: run `python setup.py upload`. This will create a git tag and publish on PyPI.

## End words

If you have questions or problems, you can [submit an issue](https://github.com/EpocDotFr/pyopml/issues).

You can also submit pull requests. It's open-source man!
