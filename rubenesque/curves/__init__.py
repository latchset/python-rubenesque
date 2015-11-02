# pylint: disable=line-too-long
#
# Copyright (c) 2015, Red Hat, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from . import base
from . import brainpool
from . import cfrg
from . import sec


def by_name(name, cls=None):
    """Returns a point class for the given curve name

    >>> by_name('secp192r1')
    <class 'rubenesque.curves.sec.secp192r1'>
    >>> by_name('snoopyCurve')
    """

    if cls is None:
        cls = base.Point

    if cls.__name__ == name:
        return cls

    for c in cls.__subclasses__():
        cc = by_name(name, c)
        if cc is not None:
            return cc

    return None


def by_oid(oid, cls=None):
    """Returns a point class for the given curve OID

    >>> by_oid((1, 2, 840, 10045, 3, 1, 1))
    <class 'rubenesque.curves.sec.secp192r1'>
    >>> by_oid((1, 2, 3, 4, 5))
    """

    if cls is None:
        cls = base.Point

    if cls.oid == oid:
        return cls

    for c in cls.__subclasses__():
        cc = by_oid(oid, c)
        if cc is not None:
            return cc

    return None
