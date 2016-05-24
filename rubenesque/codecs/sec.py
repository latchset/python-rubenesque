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

from ..lcodec import lenc, ldec


def encode(point, compressed=True):
    """
    >>> from ..curves.mdc import MDC201601
    >>> from ..curves.sec import secp224r1, secp521r1
    >>> from ..curves.cfrg import edwards25519, edwards448

    >>> encode(MDC201601.generator())
    b'\\x03\\xcag4\\xe1\\xb5\\x9c\\x0b\\x03Y\\x81M\\xcfec\\xdaB\\x1d\\xa8\\xbc=\\x81\\xa9::~s\\xc3U\\xbd(d\\xb5'

    >>> encode(MDC201601.generator(), False)
    b"\\x04\\xcag4\\xe1\\xb5\\x9c\\x0b\\x03Y\\x81M\\xcfec\\xdaB\\x1d\\xa8\\xbc=\\x81\\xa9::~s\\xc3U\\xbd(d\\xb5\\xb6\\x81\\x88j\\x7f\\x90;\\x83\\xd8[B\\x1e\\x03\\xcb\\xcfcP\\xd7*\\xbb\\x8d'\\x13\\xe2#,%\\xbf\\xeeh6;"

    >>> encode(secp224r1.generator())
    b'\\x02\\xb7\\x0e\\x0c\\xbdk\\xb4\\xbf\\x7f2\\x13\\x90\\xb9J\\x03\\xc1\\xd3V\\xc2\\x11"42\\x80\\xd6\\x11\\\\\\x1d!'

    >>> encode(secp224r1.generator(), False)
    b'\\x04\\xb7\\x0e\\x0c\\xbdk\\xb4\\xbf\\x7f2\\x13\\x90\\xb9J\\x03\\xc1\\xd3V\\xc2\\x11"42\\x80\\xd6\\x11\\\\\\x1d!\\xbd7c\\x88\\xb5\\xf7#\\xfbL"\\xdf\\xe6\\xcdCu\\xa0Z\\x07GdD\\xd5\\x81\\x99\\x85\\x00~4'

    >>> encode(secp521r1.generator())
    b"\\x02\\x00\\xc6\\x85\\x8e\\x06\\xb7\\x04\\x04\\xe9\\xcd\\x9e>\\xcbf#\\x95\\xb4B\\x9cd\\x819\\x05?\\xb5!\\xf8(\\xaf`kM=\\xba\\xa1K^w\\xef\\xe7Y(\\xfe\\x1d\\xc1'\\xa2\\xff\\xa8\\xde3H\\xb3\\xc1\\x85jB\\x9b\\xf9~~1\\xc2\\xe5\\xbdf"

    >>> encode(secp521r1.generator(), False)
    b"\\x04\\x00\\xc6\\x85\\x8e\\x06\\xb7\\x04\\x04\\xe9\\xcd\\x9e>\\xcbf#\\x95\\xb4B\\x9cd\\x819\\x05?\\xb5!\\xf8(\\xaf`kM=\\xba\\xa1K^w\\xef\\xe7Y(\\xfe\\x1d\\xc1'\\xa2\\xff\\xa8\\xde3H\\xb3\\xc1\\x85jB\\x9b\\xf9~~1\\xc2\\xe5\\xbdf\\x01\\x189)jx\\x9a;\\xc0\\x04\\\\\\x8a_\\xb4,}\\x1b\\xd9\\x98\\xf5DIW\\x9bDh\\x17\\xaf\\xbd\\x17'>f,\\x97\\xeer\\x99^\\xf4&@\\xc5P\\xb9\\x01?\\xad\\x07a5<p\\x86\\xa2r\\xc2@\\x88\\xbe\\x94v\\x9f\\xd1fP"

    >>> encode(edwards25519.generator())
    b'\\x02fffffffffffffffffffffffffffffffX'

    >>> encode(edwards25519.generator(), False)
    b'\\x04fffffffffffffffffffffffffffffffX!i6\\xd3\\xcdnS\\xfe\\xc0\\xa4\\xe21\\xfd\\xd6\\xdc\\\\i,\\xc7`\\x95%\\xa7\\xb2\\xc9V-`\\x8f%\\xd5\\x1a'

    >>> encode(edwards448.generator())
    b'\\x02\\x7f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\x7f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xfe'

    >>> encode(edwards448.generator(), False)
    b'\\x04\\x7f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\x7f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xfey\\xa7\\x0b+p@\\x05S\\xae|\\x9d\\xf4\\x16\\xc7\\x92\\xc6\\x11(u\\x1a\\xc9)i$\\x0c%\\xa0}r\\x8b\\xdc\\x93\\xe2\\x1fw\\x87\\xedir$\\x9d\\xe72\\xf3\\x84\\x96\\xcd\\x11i\\x87\\x13\\t>\\x9c\\x04\\xfc'
    """
    assert not point.is_identity

    l = (point.bits() + 7) // 8
    p = lenc(point.primary, l)

    if compressed:
        return lenc(point.secondary & 1 | 2, 1) + p
    else:
        return b'\x04' + p + lenc(point.secondary, l)


def decode(cls, bytes):
    """
    >>> from ..curves.mdc import MDC201601
    >>> from ..curves.sec import secp224r1, secp521r1
    >>> from ..curves.cfrg import edwards25519, edwards448

    >>> decode(MDC201601, encode(MDC201601.generator()))
    MDC201601(B681886A7F903B83D85B421E03CBCF6350D72ABB8D2713E2232C25BFEE68363B, CA6734E1B59C0B0359814DCF6563DA421DA8BC3D81A93A3A7E73C355BD2864B5)

    >>> decode(MDC201601, encode(MDC201601.generator(), False))
    MDC201601(B681886A7F903B83D85B421E03CBCF6350D72ABB8D2713E2232C25BFEE68363B, CA6734E1B59C0B0359814DCF6563DA421DA8BC3D81A93A3A7E73C355BD2864B5)

    >>> decode(secp224r1, encode(secp224r1.generator()))
    secp224r1(B70E0CBD6BB4BF7F321390B94A03C1D356C21122343280D6115C1D21, BD376388B5F723FB4C22DFE6CD4375A05A07476444D5819985007E34)

    >>> decode(secp224r1, encode(secp224r1.generator(), False))
    secp224r1(B70E0CBD6BB4BF7F321390B94A03C1D356C21122343280D6115C1D21, BD376388B5F723FB4C22DFE6CD4375A05A07476444D5819985007E34)

    >>> decode(secp521r1, encode(secp521r1.generator()))
    secp521r1(00C6858E06B70404E9CD9E3ECB662395B4429C648139053FB521F828AF606B4D3DBAA14B5E77EFE75928FE1DC127A2FFA8DE3348B3C1856A429BF97E7E31C2E5BD66, 011839296A789A3BC0045C8A5FB42C7D1BD998F54449579B446817AFBD17273E662C97EE72995EF42640C550B9013FAD0761353C7086A272C24088BE94769FD16650)

    >>> decode(secp521r1, encode(secp521r1.generator(), False))
    secp521r1(00C6858E06B70404E9CD9E3ECB662395B4429C648139053FB521F828AF606B4D3DBAA14B5E77EFE75928FE1DC127A2FFA8DE3348B3C1856A429BF97E7E31C2E5BD66, 011839296A789A3BC0045C8A5FB42C7D1BD998F54449579B446817AFBD17273E662C97EE72995EF42640C550B9013FAD0761353C7086A272C24088BE94769FD16650)

    >>> decode(edwards25519, encode(edwards25519.generator()))
    edwards25519(216936D3CD6E53FEC0A4E231FDD6DC5C692CC7609525A7B2C9562D608F25D51A, 6666666666666666666666666666666666666666666666666666666666666658)

    >>> decode(edwards25519, encode(edwards25519.generator(), False))
    edwards25519(216936D3CD6E53FEC0A4E231FDD6DC5C692CC7609525A7B2C9562D608F25D51A, 6666666666666666666666666666666666666666666666666666666666666658)

    >>> decode(edwards448, encode(edwards448.generator()))
    edwards448(79A70B2B70400553AE7C9DF416C792C61128751AC92969240C25A07D728BDC93E21F7787ED6972249DE732F38496CD11698713093E9C04FC, 7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE)

    >>> decode(edwards448, encode(edwards448.generator(), False))
    edwards448(79A70B2B70400553AE7C9DF416C792C61128751AC92969240C25A07D728BDC93E21F7787ED6972249DE732F38496CD11698713093E9C04FC, 7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE)
    """
    assert bytes.startswith((b'\x02', b'\x03', b'\x04'))

    l = (cls.bits() + 7) // 8
    z = bytes[0] if isinstance(bytes[0], int) else ord(bytes[0])
    p = ldec(bytes[1:l + 1])
    if z == 4:
        s = ldec(bytes[l + 1:2 * l + 1])
        point = cls.create(p, s)
    else:
        point = cls.recover(p, z & 1)

    assert point.is_valid
    return point
