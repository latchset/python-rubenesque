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

import abc

from ..math import sqrt, inv
from .prime import Point


class Point(Point):
    a = 1
    d = 1

    @classmethod
    def create(cls, primary, secondary):
        return cls(secondary, primary)

    @classmethod
    def recover(cls, primary, bit):
        pp = primary * primary % cls.prime
        a = (pp - 1) % cls.prime
        b = (cls.d * pp % cls.prime - cls.a) % cls.prime
        s = sqrt(a * inv(b, cls.prime), cls.prime)
        assert s != 0

        secondary = s if s & 1 == bit else ((cls.prime - s) % cls.prime)
        return cls(secondary, primary)

    def __init__(self, x=None, y=None, z=1, t=None):
        assert (y is None and x is None) \
            or (y is not None and x is not None)

        self.__x = 0 if x is None else x
        self.__y = 1 if y is None else y
        self.__z = z
        self.__t = t if t is not None else (
            self.__x * self.__y % self.__class__.prime
                     * self.__z % self.__class__.prime
        )

    def __normalize(self):
        if self.__z in (0, 1):
            return

        p = self.__class__.prime
        self.__x = self.__x * inv(self.__z, p) % p
        self.__y = self.__y * inv(self.__z, p) % p
        self.__z = 1
        self.__t = self.__x * self.__y

    @property
    def is_identity(self):
        return self.__z == 0 or self.__x == 0 and self.__y == self.__z

    @property
    def is_valid(self):
        if self.is_identity:
            return False

        p = self.__class__.prime

        yy = self.y * self.y % p
        xx = self.x * self.x % p

        l = (self.__class__.a * xx % p + yy) % p
        r = (1 + self.__class__.d * xx % p * yy % p) % p

        return l == r

    @property
    def x(self):
        self.__normalize()
        return self.__x if self.__z == 1 else None

    @property
    def y(self):
        self.__normalize()
        return self.__y if self.__z == 1 else None

    @property
    def primary(self):
        return self.y

    @property
    def secondary(self):
        return self.x

    def __eq__(self, other):
        p = self.__class__.prime
        x = other.__x * self.__z % p == self.__x * other.__z % p
        y = other.__y * self.__z % p == self.__y * other.__z % p
        return x and y

    def __add__(self, other):
        assert isinstance(other, self.__class__)

        if self.is_identity or other.is_identity:
            return self if other.is_identity else other

        p = self.__class__.prime

        if self == other:
            # https://www.hyperelliptic.org/EFD/g1p/auto-twisted-extended.html#doubling-dbl-2008-hwcd
            A = self.__x * self.__x % p
            B = self.__y * self.__y % p
            C = 2 * self.__z % p * self.__z % p
            D = self.__class__.a * A % p
            E = ((pow((self.__x + self.__y) % p, 2, p) - A) % p - B) % p
            G = (D + B) % p
            F = (G - C) % p
            H = (D - B) % p
        else:
            # https://www.hyperelliptic.org/EFD/g1p/auto-twisted-extended.html#addition-add-2008-hwcd-2
            A = self.__x * other.__x % p
            B = self.__y * other.__y % p
            C = self.__z * other.__t % p
            D = self.__t * other.__z % p
            E = (D + C) % p
            F = ((((self.__x - self.__y) % p) * ((other.__x + other.__y) % p) % p + B) % p - A) % p
            G = (B + self.__class__.a * A % p) % p
            H = (D - C) % p

        X3 = E * F % p
        Y3 = G * H % p
        T3 = E * H % p
        Z3 = F * G % p
        return self.__class__(X3, Y3, Z3, T3)
