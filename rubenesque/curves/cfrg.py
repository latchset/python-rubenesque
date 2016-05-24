# -*- coding: utf-8 -*-
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

from .edwards import Point


class edwards25519(Point):
    """
    >>> from . import find
    >>> cls = find("edwards25519")
    >>> find("ed25519")
    <class 'rubenesque.curves.cfrg.edwards25519'>

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


    >>> edwards25519.generator()
    edwards25519(216936D3CD6E53FEC0A4E231FDD6DC5C692CC7609525A7B2C9562D608F25D51A, 6666666666666666666666666666666666666666666666666666666666666658)

    >>> edwards25519.generator() * 0x449a44ba44226a50185afcc10a4c1462dd5e46824b15163b9d7c52f06be346a0
    edwards25519(1229EF6103B0AB43012C2DA513CC07CDB72A5DD0C37B3813D781B195A1BA7166, 1CC8FD645E6144B78000B7AEAE4A382FBAB72A08F9B6FB8A92C1BF3D7A032DBB)

    >>> edwards25519.generator() + edwards25519.generator() * 0x449a44ba44226a50185afcc10a4c1462dd5e46824b15163b9d7c52f06be346a0
    edwards25519(3318E20DB2054DE4687BADC30CC6BDC7406069B0DC3CD9F65E2ECBA364E4A077, 4641AE96F530129FA2107E9B79ED5893AD03C4EDDBFDB444ABC76FF629C6A973)
    """

    a = -1
    d = 0x52036cee2b6ffe738cc740797779e89800700a4d4141d8ab75eb4dca135978a3
    order = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
    prime = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed
    aliases = ("ed25519", )
    cofactor = 8

    @classmethod
    def generator(cls):
        return cls(
            0x216936d3cd6e53fec0a4e231fdd6dc5c692cc7609525a7b2c9562d608f25d51a,
            0x6666666666666666666666666666666666666666666666666666666666666658
        )


class edwards448(Point):
    """
    >>> from . import find
    >>> cls = find("edwards448")
    >>> find("ed448")
    <class 'rubenesque.curves.cfrg.edwards448'>

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

    >>> edwards448.generator()
    edwards448(79A70B2B70400553AE7C9DF416C792C61128751AC92969240C25A07D728BDC93E21F7787ED6972249DE732F38496CD11698713093E9C04FC, 7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE)

    >>> edwards448.generator() * 0
    edwards448(∞)
    >>> edwards448.generator() * 1
    edwards448(79A70B2B70400553AE7C9DF416C792C61128751AC92969240C25A07D728BDC93E21F7787ED6972249DE732F38496CD11698713093E9C04FC, 7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE)
    >>> edwards448.generator() + edwards448.generator() * 0
    edwards448(79A70B2B70400553AE7C9DF416C792C61128751AC92969240C25A07D728BDC93E21F7787ED6972249DE732F38496CD11698713093E9C04FC, 7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE)

    TODO: More test vectors needed...
    """

    d = 0xd78b4bdc7f0daf19f24f38c29373a2ccad46157242a50f37809b1da3412a12e79ccc9c81264cfe9ad080997058fb61c4243cc32dbaa156b9
    order = 0x3fffffffffffffffffffffffffffffffffffffffffffffffffffffff7cca23e9c44edb49aed63690216cc2728dc58f552378c292ab5844f3
    prime = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    aliases = ("ed448", )
    cofactor = 4

    @classmethod
    def generator(cls):
        return cls(
            0x79a70b2b70400553ae7c9df416c792c61128751ac92969240c25a07d728bdc93e21f7787ed6972249de732f38496cd11698713093e9c04fc,
            0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffff7ffffffffffffffffffffffffffffffffffffffffffffffffffffffe
        )
