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

from .weierstrass import Point


class secp192r1(Point):
    """
    >>> from . import find
    >>> cls = find("secp192r1")
    >>> find("1.2.840.10045.3.1.1")
    <class 'rubenesque.curves.sec.secp192r1'>

    Test basic math:
    >>> cls().is_identity
    True
    >>> (-cls()).is_identity
    True
    >>> cls().is_valid
    False
    >>> (cls.generator() * 0).is_identity
    True
    >>> cls.generator() * 1 == cls.generator()
    True
    >>> cls.generator() + cls.generator() * 0 == cls.generator()
    True
    >>> cls.generator() + cls.generator() == cls.generator() * 2
    True
    >>> cls.generator() * 2 + cls.generator() == cls.generator() * 3
    True
    >>> cls.generator() * 2 - cls.generator() == cls.generator()
    True
    >>> cls.generator() * 6 / 3 == cls.generator() * 2
    True

    >>> a = secp192r1.generator() * 0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D2282F
    >>> a
    secp192r1(DAFEBF5828783F2AD35534631588A3F629A70FB16982A888, 229425F266C25F05B94D8443EBE4796FA6CCE505A3816C54)
    >>> b = secp192r1.generator() * 0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22830
    >>> b
    secp192r1(188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012, F8E6D46A003725879CEFEE1294DB32298C06885EE186B7EE)
    >>> c = a * 0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22830
    >>> c
    secp192r1(DAFEBF5828783F2AD35534631588A3F629A70FB16982A888, DD6BDA0D993DA0FA46B27BBC141B868F59331AFA5C7E93AB)
    >>> b * 0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D2282F == c
    True
    """

    a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
    b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
    order = 0xffffffffffffffffffffffff99def836146bc9b1b4d22831
    prime = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
    aliases = ("1.2.840.10045.3.1.1", )

    @classmethod
    def generator(cls):
        return cls(
            0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012,
            0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811
        )


class secp224r1(Point):
    """
    >>> from . import find
    >>> cls = find("secp224r1")
    >>> find("1.3.132.0.33")
    <class 'rubenesque.curves.sec.secp224r1'>

    Test basic math:
    >>> cls().is_identity
    True
    >>> (-cls()).is_identity
    True
    >>> cls().is_valid
    False
    >>> (cls.generator() * 0).is_identity
    True
    >>> cls.generator() * 1 == cls.generator()
    True
    >>> cls.generator() + cls.generator() * 0 == cls.generator()
    True
    >>> cls.generator() + cls.generator() == cls.generator() * 2
    True
    >>> cls.generator() * 2 + cls.generator() == cls.generator() * 3
    True
    >>> cls.generator() * 2 - cls.generator() == cls.generator()
    True
    >>> cls.generator() * 6 / 3 == cls.generator() * 2
    True

    >>> a = secp224r1.generator() * 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFF16A2E0B8F03E13DD29455C5C2A3B
    >>> a
    secp224r1(706A46DC76DCB76798E60E6D89474788D16DC18032D268FD1A704FA6, E3D4895843DA188FD58FB0567976D7B50359D6B78530C8F62D1B1746)
    >>> b = secp224r1.generator() * 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFF16A2E0B8F03E13DD29455C5C2A3C
    >>> b
    secp224r1(B70E0CBD6BB4BF7F321390B94A03C1D356C21122343280D6115C1D21, 42C89C774A08DC04B3DD201932BC8A5EA5F8B89BBB2A7E667AFF81CD)
    >>> c = b * 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFF16A2E0B8F03E13DD29455C5C2A3B
    >>> c
    secp224r1(706A46DC76DCB76798E60E6D89474788D16DC18032D268FD1A704FA6, 1C2B76A7BC25E7702A704FA986892849FCA629487ACF3709D2E4E8BB)
    >>> a * 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFF16A2E0B8F03E13DD29455C5C2A3C == c
    True
    """

    a = 0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe
    b = 0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4
    order = 0xffffffffffffffffffffffffffff16a2e0b8f03e13dd29455c5c2a3d
    prime = 0xffffffffffffffffffffffffffffffff000000000000000000000001
    aliases = ("1.3.132.0.33", )

    @classmethod
    def generator(cls):
        return cls(
            0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21,
            0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34
        )


class secp256r1(Point):
    """
    >>> from . import find
    >>> cls = find("secp256r1")
    >>> find("1.2.840.10045.3.1.7")
    <class 'rubenesque.curves.sec.secp256r1'>
    >>> find("P256")
    <class 'rubenesque.curves.sec.secp256r1'>
    >>> find("P-256")
    <class 'rubenesque.curves.sec.secp256r1'>

    Test basic math:
    >>> cls().is_identity
    True
    >>> (-cls()).is_identity
    True
    >>> cls().is_valid
    False
    >>> (cls.generator() * 0).is_identity
    True
    >>> cls.generator() * 1 == cls.generator()
    True
    >>> cls.generator() + cls.generator() * 0 == cls.generator()
    True
    >>> cls.generator() + cls.generator() == cls.generator() * 2
    True
    >>> cls.generator() * 2 + cls.generator() == cls.generator() * 3
    True
    >>> cls.generator() * 2 - cls.generator() == cls.generator()
    True
    >>> cls.generator() * 6 / 3 == cls.generator() * 2
    True

    >>> a = secp256r1.generator() * 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC63254F
    >>> a
    secp256r1(7CF27B188D034F7E8A52380304B51AC3C08969E277F21B35A60B48FC47669978, F888AAEE24712FC0D6C26539608BCF244582521AC3167DD661FB4862DD878C2E)
    >>> b = secp256r1.generator() * 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632550
    >>> b
    secp256r1(6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296, B01CBD1C01E58065711814B583F061E9D431CCA994CEA1313449BF97C840AE0A)
    >>> c = a * 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632550
    >>> c
    secp256r1(7CF27B188D034F7E8A52380304B51AC3C08969E277F21B35A60B48FC47669978, 07775510DB8ED040293D9AC69F7430DBBA7DADE63CE982299E04B79D227873D1)
    >>> b * 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC63254F == c
    True
    """

    a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
    b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
    order = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
    prime = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
    aliases = ("1.2.840.10045.3.1.7", "P256", "P-256")

    @classmethod
    def generator(cls):
        return cls(
            0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
            0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
        )


class secp384r1(Point):
    """
    >>> from . import find
    >>> cls = find("secp384r1")
    >>> find("1.3.132.0.34")
    <class 'rubenesque.curves.sec.secp384r1'>
    >>> find("P384")
    <class 'rubenesque.curves.sec.secp384r1'>
    >>> find("P-384")
    <class 'rubenesque.curves.sec.secp384r1'>

    Test basic math:
    >>> cls().is_identity
    True
    >>> (-cls()).is_identity
    True
    >>> cls().is_valid
    False
    >>> (cls.generator() * 0).is_identity
    True
    >>> cls.generator() * 1 == cls.generator()
    True
    >>> cls.generator() + cls.generator() * 0 == cls.generator()
    True
    >>> cls.generator() + cls.generator() == cls.generator() * 2
    True
    >>> cls.generator() * 2 + cls.generator() == cls.generator() * 3
    True
    >>> cls.generator() * 2 - cls.generator() == cls.generator()
    True
    >>> cls.generator() * 6 / 3 == cls.generator() * 2
    True

    >>> a = secp384r1.generator() * 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52971
    >>> a
    secp384r1(08D999057BA3D2D969260045C55B97F089025959A6F434D651D207D19FB96E9E4FE0E86EBE0E64F85B96A9C75295DF61, 717F0E05A4E4C312484017200292458B4D8A278A43933BC16FB1AFA0DA954BD9A002BC15B2C61DD29EAFE190F56BF17F)
    >>> b = secp384r1.generator() * 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52972
    >>> b
    secp384r1(AA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB7, C9E821B569D9D390A26167406D6D23D6070BE242D765EB831625CEEC4A0F473EF59F4E30E2817E6285BCE2846F15F1A0)
    >>> c = a * 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52972
    >>> c
    secp384r1(08D999057BA3D2D969260045C55B97F089025959A6F434D651D207D19FB96E9E4FE0E86EBE0E64F85B96A9C75295DF61, 8E80F1FA5B1B3CEDB7BFE8DFFD6DBA74B275D875BC6CC43E904E505F256AB4255FFD43E94D39E22D61501E700A940E80)
    >>> b * 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52971 == c
    True
    """

    a = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000fffffffc
    b =  0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef
    order = 0xffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52973
    prime = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000ffffffff
    aliases = ("1.3.132.0.34", "P384", "P-384")

    @classmethod
    def generator(cls):
        return cls(
            0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7,
            0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f
        )


class secp521r1(Point):
    """
    >>> from . import find
    >>> cls = find("secp521r1")
    >>> find("1.3.132.0.35")
    <class 'rubenesque.curves.sec.secp521r1'>
    >>> find("P521")
    <class 'rubenesque.curves.sec.secp521r1'>
    >>> find("P-521")
    <class 'rubenesque.curves.sec.secp521r1'>

    Test basic math:
    >>> cls().is_identity
    True
    >>> (-cls()).is_identity
    True
    >>> cls().is_valid
    False
    >>> (cls.generator() * 0).is_identity
    True
    >>> cls.generator() * 1 == cls.generator()
    True
    >>> cls.generator() + cls.generator() * 0 == cls.generator()
    True
    >>> cls.generator() + cls.generator() == cls.generator() * 2
    True
    >>> cls.generator() * 2 + cls.generator() == cls.generator() * 3
    True
    >>> cls.generator() * 2 - cls.generator() == cls.generator()
    True
    >>> cls.generator() * 6 / 3 == cls.generator() * 2
    True

    >>> a = secp521r1.generator() * 0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA51868783BF2F966B7FCC0148F709A5D03BB5C9B8899C47AEBB6FB71E91386407
    >>> a
    secp521r1(00433C219024277E7E682FCB288148C282747403279B1CCC06352C6E5505D769BE97B3B204DA6EF55507AA104A3A35C5AF41CF2FA364D60FD967F43E3933BA6D783D, 010B44733807924D98FF580C1311112C0F4A394AEF83B25688BF54DE5D66F93BD2444C1C882160DAE0946C6C805665CDB70B1503416A123F0B08E41CA9299E0BE4FD)
    >>> b = secp521r1.generator() * 0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA51868783BF2F966B7FCC0148F709A5D03BB5C9B8899C47AEBB6FB71E91386408
    >>> b
    secp521r1(00C6858E06B70404E9CD9E3ECB662395B4429C648139053FB521F828AF606B4D3DBAA14B5E77EFE75928FE1DC127A2FFA8DE3348B3C1856A429BF97E7E31C2E5BD66, 00E7C6D6958765C43FFBA375A04BD382E426670ABBB6A864BB97E85042E8D8C199D368118D66A10BD9BF3AAF46FEC052F89ECAC38F795D8D3DBF77416B89602E99AF)
    >>> c = a * 0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA51868783BF2F966B7FCC0148F709A5D03BB5C9B8899C47AEBB6FB71E91386408
    >>> c
    secp521r1(00433C219024277E7E682FCB288148C282747403279B1CCC06352C6E5505D769BE97B3B204DA6EF55507AA104A3A35C5AF41CF2FA364D60FD967F43E3933BA6D783D, 00F4BB8CC7F86DB26700A7F3ECEEEED3F0B5C6B5107C4DA97740AB21A29906C42DBBB3E377DE9F251F6B93937FA99A3248F4EAFCBE95EDC0F4F71BE356D661F41B02)
    >>> b * 0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA51868783BF2F966B7FCC0148F709A5D03BB5C9B8899C47AEBB6FB71E91386407 == c
    True
    """

    a = 0x000001fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc
    b = 0x00000051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00
    order = 0x000001fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409
    prime = 0x000001ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    aliases = ("1.3.132.0.35", "P521", "P-521")

    @classmethod
    def generator(cls):
        return cls(
            0x000000c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66,
            0x0000011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650
        )
