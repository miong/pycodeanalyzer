pycodeanalyzer
==============
.. image:: https://img.shields.io/badge/status-active-green
    :alt: Status - active
.. image:: https://img.shields.io/pypi/pyversions/pycodeanalyzer
    :target: https://pypi.python.org/pypi/pycodeanalyzer
    :alt: Python version
.. image:: https://img.shields.io/pypi/l/pycodeanalyzer
    :target: https://raw.githubusercontent.com/miong/pycodeanalyzer/main/LICENSE
    :alt: License
.. image:: https://img.shields.io/pypi/v/pycodeanalyzer.svg
    :target: https://pypi.python.org/pypi/pycodeanalyzer
    :alt: Latest PyPI version
.. image:: https://img.shields.io/badge/TestPyPi-Latest-blue
   :target: https://test.pypi.org/project/pycodeanalyzer/
   :alt: TestPyPI
.. image:: https://github.com/miong/pycodeanalyzer/actions/workflows/unittests.yml/badge.svg
    :alt: Unit tests
.. image:: https://github.com/miong/pycodeanalyzer/actions/workflows/quality.yml/badge.svg
    :alt: Code Quality

Code analyzer to get information to help developers to understand how projects works.

Installation
------------

pycodeanlyzer is available on PyPI::

        pip install pycodeanalyzer

see https://pip.pypa.io/en/stable/installation/ for more detail on pip

Requirements
^^^^^^^^^^^^

- .. image:: https://img.shields.io/static/v1?label=robotpy-cppheaderparser&message=equals%205.0.16&color=blue
    :alt: - robotpy-cppheaderparser - equals 5.0.16
- .. image:: https://img.shields.io/static/v1?label=Flask&message=equals%202.0.3&color=blue
    :alt: - Flask - equals 2.0.3
- .. image:: https://img.shields.io/static/v1?label=Flask-SocketIO&message=equals%205.1.1&color=blue
    :alt: - Flask-SocketIO - equals 5.1.1
- .. image:: https://img.shields.io/static/v1?label=Flask-Classful&message=equals%200.14.2&color=blue
    :alt: - Flask-Classful - equals 0.14.2
- .. image:: https://img.shields.io/static/v1?label=flaskwebgui&message=equals%200.3.4&color=blue
    :alt: - flaskwebgui - equals 0.3.4
- .. image:: https://img.shields.io/static/v1?label=simple-websocket&message=equals%200.5.1&color=blue
    :alt: - simple-websocket - equals 0.5.1
- .. image:: https://img.shields.io/static/v1?label=injector&message=equals%200.19.0&color=blue
    :alt: - injector - equals 0.19.0
- .. image:: https://img.shields.io/static/v1?label=pathlib&message=equals%201.0.1&color=blue
    :alt: - pathlib - equals 1.0.1
- .. image:: https://img.shields.io/static/v1?label=python-magic&message=equals%200.4.25&color=blue
    :alt: - python-magic - equals 0.4.25
- .. image:: https://img.shields.io/static/v1?label=pcpp&message=equals%201.30&color=blue
    :alt: - pcpp - equals 1.30
- .. image:: https://img.shields.io/static/v1?label=pytest&message=the%20latest&color=blue
    :alt: - pytest - the latest
- .. image:: https://img.shields.io/static/v1?label=pytest-cov&message=the%20latest&color=blue
    :alt: - pytest-cov - the latest

Usage
-----
The following is the help of pycodeanalyzer::

	usage: pycodeanalyzer [-h] [--log LOGLEVEL] path
	
	positional arguments:
	  path            Path of the root directory to be analysed
	
	optional arguments:
	  -h, --help      show this help message and exit
	  --log LOGLEVEL  Log level to be used

To get more information during the run, use --log=DEBUG

Languages
---------

pycodeanalyser supports the following languages:

- C/C++

Licence
-------

This project is under the MIT license::

    The MIT License (MIT)

    Copyright (c) 2022 Giovanni Mion

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

Authors
-------

`pycodeanalyzer` was written by `Giovanni Mion <mion.ggb@gmail.com>`_.
