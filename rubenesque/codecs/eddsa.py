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


def encode(point):
    """
    >>> from ..curves.sec import secp224r1, secp521r1
    >>> from ..curves.cfrg import edwards25519

    >>> encode(secp224r1.generator())
    Traceback (most recent call last):
    AssertionError: assert (224 % 8) > 0

    >>> encode(secp521r1.generator())
    b"f\\xbd\\xe5\\xc21~~\\xf9\\x9bBj\\x85\\xc1\\xb3H3\\xde\\xa8\\xff\\xa2'\\xc1\\x1d\\xfe(Y\\xe7\\xefw^K\\xa1\\xba=Mk`\\xaf(\\xf8!\\xb5?\\x059\\x81d\\x9cB\\xb4\\x95#f\\xcb>\\x9e\\xcd\\xe9\\x04\\x04\\xb7\\x06\\x8e\\x85\\xc6\\x00"

    >>> encode(edwards25519.generator())
    b'Xfffffffffffffffffffffffffffffff'
    """
    assert point.bits() % 8 > 0

    i = point.primary | ((point.secondary & 1) << point.bits())
    return i.to_bytes((point.bits() + 7) // 8, 'little')


def decode(cls, bytes):
    """
    >>> from ..curves.sec import secp224r1, secp521r1
    >>> from ..curves.cfrg import edwards25519

    >>> decode(secp521r1, encode(secp521r1.generator()))
    secp521r1(00C6858E06B70404E9CD9E3ECB662395B4429C648139053FB521F828AF606B4D3DBAA14B5E77EFE75928FE1DC127A2FFA8DE3348B3C1856A429BF97E7E31C2E5BD66, 011839296A789A3BC0045C8A5FB42C7D1BD998F54449579B446817AFBD17273E662C97EE72995EF42640C550B9013FAD0761353C7086A272C24088BE94769FD16650)

    >>> decode(edwards25519, encode(edwards25519.generator()))
    edwards25519(6666666666666666666666666666666666666666666666666666666666666658, 216936D3CD6E53FEC0A4E231FDD6DC5C692CC7609525A7B2C9562D608F25D51A)
    """
    assert len(bytes) == (cls.bits() + 7) // 8
    assert cls.bits() % 8 > 0

    mask = 1 << cls.bits()
    primary = int.from_bytes(bytes, 'little')
    bit = primary & mask >> cls.bits()
    primary &= ~mask

    point = cls.recover(primary, bit)
    point.is_valid
    return point
