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

from ..math import inv
from ..lcodec import ldec


def sign(cls, prv, hsh, testk=None):
    """
    Test values are from RFC 4754

    >>> from rubenesque.curves.sec import secp256r1, secp384r1, secp521r1
    >>> from hashlib import sha256, sha384, sha512


    >>> h = sha256(b'abc').digest()
    >>> w = 0xDC51D3866A15BACDE33D96F992FCA99DA7E6EF0934E7097559C27F1614C88A7F
    >>> k = 0x9E56F509196784D963D1C0A401510EE7ADA3DCC5DEE04B154BF61AF1D5A6DECE
    >>> a, b = sign(secp256r1, w, h, k)
    >>> a == 91891732277435504623317252591401134119269651937436268244947074415855034340732
    True
    >>> b == 61052045556022437972545958544857058931480303283285058697354104476845267944213
    True


    >>> h = sha384(b'abc').digest()
    >>> w = 0x0BEB646634BA87735D77AE4809A0EBEA865535DE4C1E1DCB692E84708E81A5AF62E528C38B2A81B35309668D73524D9F
    >>> k = 0xB4B74E44D71A13D568003D7489908D564C7761E229C58CBFA18950096EB7463B854D7FA992F934D927376285E63414FA
    >>> a, b = sign(secp384r1, w, h, k)
    >>> a == 38633327193540170134142746196640777001610571660897807027400558946617577572929271756342333545057439198888737488858803
    True
    >>> b == 27456607455725262996851015520164417800230371254197279025501184027627966373822115908168123099250660377810276830841759
    True


    >>> h = sha512(b'abc').digest()
    >>> w = 0x0065FDA3409451DCAB0A0EAD45495112A3D813C17BFD34BDF8C1209D7DF5849120597779060A7FF9D704ADF78B570FFAD6F062E95C7E0C5D5481C5B153B48B375FA1
    >>> k = 0x00C1C2B305419F5A41344D7E4359933D734096F556197A9B244342B8B62F46F9373778F9DE6B6497B1EF825FF24F42F9B4A4BD7382CFC3378A540B1B7F0C1B956C2F
    >>> a, b = sign(secp521r1, w, h, k)
    >>> a == 4571916881931522509684395052881421199225740839880572005887744882418558877708584528579508021653311389814949506911518722326141413326277238174509287981280731729
    True
    >>> b == 5028224013397087880963813951950174050813517229556618035427576214486083823861825258909909585187151444995522339222016536225541889721370155815222553876665673312
    True
    """
    assert prv >= 1 and prv < cls.order

    z = ldec(hsh) & (2 ** cls.bits() - 1)
    while True:
        k = cls.private_key() if testk is None else testk
        r = (cls.generator() * k).primary % cls.order
        s = inv(k, cls.order) * (z + r * prv % cls.order) % cls.order
        if r != 0 and s != 0:
            return (r, s)


def verify(pub, hsh, r, s):
    """
    Test values are from RFC 4754

    >>> from rubenesque.curves.sec import secp256r1, secp384r1, secp521r1
    >>> from hashlib import sha256, sha384, sha512


    >>> h = sha256(b'abc').digest()
    >>> w = 0xDC51D3866A15BACDE33D96F992FCA99DA7E6EF0934E7097559C27F1614C88A7F
    >>> r = 0xCB28E0999B9C7715FD0A80D8E47A77079716CBBF917DD72E97566EA1C066957C
    >>> s = 0x86FA3BB4E26CAD5BF90B7F81899256CE7594BB1EA0C89212748BFF3B3D5B0315
    >>> verify(secp256r1.generator() * w, h, r, s)
    True
    >>> verify(secp256r1.generator() * secp256r1.order, h, r, s)
    False
    >>> verify(secp256r1.generator() * w, h, r, 0)
    False
    >>> verify(secp256r1.generator() * w, h, 0, s)
    False


    >>> h = sha384(b'abc').digest()
    >>> w = 0x0BEB646634BA87735D77AE4809A0EBEA865535DE4C1E1DCB692E84708E81A5AF62E528C38B2A81B35309668D73524D9F
    >>> r = 0xFB017B914E29149432D8BAC29A514640B46F53DDAB2C69948084E2930F1C8F7E08E07C9C63F2D21A07DCB56A6AF56EB3
    >>> s = 0xB263A1305E057F984D38726A1B46874109F417BCA112674C528262A40A629AF1CBB9F516CE0FA7D2FF630863A00E8B9F
    >>> verify(secp384r1.generator() * w, h, r, s)
    True
    >>> verify(secp384r1.generator() * secp384r1.order, h, r, s)
    False
    >>> verify(secp384r1.generator() * w, h, r, 0)
    False
    >>> verify(secp384r1.generator() * w, h, 0, s)
    False


    >>> h = sha512(b'abc').digest()
    >>> w = 0x0065FDA3409451DCAB0A0EAD45495112A3D813C17BFD34BDF8C1209D7DF5849120597779060A7FF9D704ADF78B570FFAD6F062E95C7E0C5D5481C5B153B48B375FA1
    >>> r = 0x0154FD3836AF92D0DCA57DD5341D3053988534FDE8318FC6AAAAB68E2E6F4339B19F2F281A7E0B22C269D93CF8794A9278880ED7DBB8D9362CAEACEE544320552251
    >>> s = 0x017705A7030290D1CEB605A9A1BB03FF9CDD521E87A696EC926C8C10C8362DF4975367101F67D1CF9BCCBF2F3D239534FA509E70AAC851AE01AAC68D62F866472660
    >>> verify(secp521r1.generator() * w, h, r, s)
    True
    >>> verify(secp521r1.generator() * secp521r1.order, h, r, s)
    False
    >>> verify(secp521r1.generator() * w, h, r, 0)
    False
    >>> verify(secp521r1.generator() * w, h, 0, s)
    False
    """

    if not pub.is_valid:
        return False

    if not (pub * pub.order).is_identity:
        return False

    if r < 1 or r >= pub.order:
        return False

    if s < 1 or s >= pub.order:
        return False

    z = ldec(hsh) & (2 ** pub.bits() - 1)
    w = inv(s, pub.order)
    u1 = z * w % pub.order
    u2 = r * w % pub.order
    p = pub.generator() * u1 + pub * u2

    return r == p.primary
