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


def find(id):
    """Returns a point class for the given curve identifier

    Identifiers can be the class name:
    >>> find('secp256r1')
    <class 'rubenesque.curves.sec.secp256r1'>
    >>> find('edwards25519')
    <class 'rubenesque.curves.cfrg.edwards25519'>

    Identifiers can be a common alias:
    >>> find('P-256')
    <class 'rubenesque.curves.sec.secp256r1'>
    >>> find('ed25519')
    <class 'rubenesque.curves.cfrg.edwards25519'>

    Identifiers can be OIDs:
    >>> find("1.2.840.10045.3.1.1")
    <class 'rubenesque.curves.sec.secp192r1'>

    >>> find('snoopyCurve')
    Traceback (most recent call last):
        ...
    NameError: Unknown curve 'snoopyCurve'
    """

    def _inner(name, cls=base.Point):
        if cls.__name__ == name:
            return cls

        if name in cls.aliases:
            return cls

        for c in cls.__subclasses__():
            cc = _inner(name, c)
            if cc is not None:
                return cc

        return None

    cls =  _inner(id)
    if cls is None:
        raise NameError("Unknown curve '%s'" % id)
    return cls

def supported():
    """Returns a list of the names of supported curves.

    >>> tuple(sorted(supported()))
    ('MDC201601', 'brainpoolP160r1', 'brainpoolP192r1', 'brainpoolP224r1', 'brainpoolP256r1', 'brainpoolP320r1', 'brainpoolP384r1', 'brainpoolP512r1', 'edwards25519', 'edwards448', 'secp192r1', 'secp224r1', 'secp256r1', 'secp384r1', 'secp521r1')
    """

    def _inner(cls=base.Point):
        if not cls.__subclasses__():
            yield cls.__name__
        else:
            for c in cls.__subclasses__():
                for n in _inner(c):
                    yield n

    return _inner()
