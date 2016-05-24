# pylint: disable=line-too-long
#
# Copyright (c) 2016, Red Hat, Inc.
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


class MDC201601(Point):
    """
    >>> from . import find
    >>> cls = find("MDC201601")

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

    >>> MDC201601.generator()
    MDC201601(B681886A7F903B83D85B421E03CBCF6350D72ABB8D2713E2232C25BFEE68363B, CA6734E1B59C0B0359814DCF6563DA421DA8BC3D81A93A3A7E73C355BD2864B5)
    """

    d = 39384817741350628573161184301225915800358770588933756071948264625804612259721
    order = 27278090819240297610677772592287387918930509574048068887630978293185521973243
    prime = 109112363276961190442711090369149551676330307646118204517771511330536253156371
    cofactor = 4

    @classmethod
    def generator(cls):
        return cls(
            82549803222202399340024462032964942512025856818700414254726364205096731424315,
            91549545637415734422658288799119041756378259523097147807813396915125932811445
        )
