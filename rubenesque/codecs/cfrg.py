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

"""
Implements codec according to the protocol discussed on CFRG:
http://www.ietf.org/mail-archive/web/cfrg/current/msg07256.html
"""

from ..lcodec import lenc, ldec


def encode(point):
    """
    >>> from ..curves.sec import secp224r1, secp521r1
    >>> from ..curves.cfrg import edwards25519, edwards448

    >>> encode(secp224r1.generator())
    b'!\\x1d\\\\\\x11\\xd6\\x8024"\\x11\\xc2V\\xd3\\xc1\\x03J\\xb9\\x90\\x132\\x7f\\xbf\\xb4k\\xbd\\x0c\\x0e\\xb7\\x00'

    >>> encode(secp521r1.generator())
    b"f\\xbd\\xe5\\xc21~~\\xf9\\x9bBj\\x85\\xc1\\xb3H3\\xde\\xa8\\xff\\xa2'\\xc1\\x1d\\xfe(Y\\xe7\\xefw^K\\xa1\\xba=Mk`\\xaf(\\xf8!\\xb5?\\x059\\x81d\\x9cB\\xb4\\x95#f\\xcb>\\x9e\\xcd\\xe9\\x04\\x04\\xb7\\x06\\x8e\\x85\\xc6\\x00"

    >>> encode(edwards25519.generator())
    b'Xfffffffffffffffffffffffffffffff'

    >>> encode(edwards448.generator())
    b'\\xfe\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\x7f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\x7f\\x00'
    """

    l = point.bits() // 8 + 1
    b = (point.secondary & 1) << (l * 8 - 1)
    return lenc(point.primary | b, l, False)


def decode(cls, bytes):
    """
    >>> from ..curves.sec import secp224r1, secp521r1
    >>> from ..curves.cfrg import edwards25519, edwards448

    >>> g5 = secp224r1.generator() * 5
    >>> decode(secp224r1, encode(g5)) == g5
    True

    >>> g5 = secp521r1.generator() * 5
    >>> decode(secp521r1, encode(g5)) == g5
    True

    >>> g5 = edwards25519.generator() * 5
    >>> decode(edwards25519, encode(g5)) == g5
    True

    >>> g5 = edwards448.generator() * 5
    >>> decode(edwards448, encode(g5)) == g5
    True
    """

    l = cls.bits() // 8 + 1
    assert len(bytes) == l

    p = ldec(bytes, False)
    b = (p >> (l * 8 - 1)) & 1
    p &= ~(1 << (l * 8 - 1))

    point = cls.recover(p, b)
    assert point.is_valid
    return point
