# Copyright (C) 2015, Red Hat, Inc.
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
from distutils.core import setup


def read(fname):
    fname = os.path.join(os.path.dirname(__file__), fname)
    with open(fname) as f:
        return f.read()


setup(
    name="rubenesque",
    version="1",
    author="Nathaniel McCallum",
    author_email="npmccallum@redhat.com",
    description=("A pure-python implementation of elliptic curves."),
    license="BSD",
    keywords="cryptography elliptic curves",
    url="http://github.com/npmccallum/python-rubenesque",
    packages=[
        'rubenesque',
        'rubenesque.codecs',
        'rubenesque.curves',
        'rubenesque.signatures',
    ],
    long_description=read('README.md'),
    requires=[],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Security :: Cryptography"
    ],
)
