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
This module implements Weierstrass curves following the methods given by
RFC 6090. In particular, we use homogeneous coordinates to avoid unnecessary
inversions.
"""

import abc

from ..math import sqrt, inv
from .prime import Point


class Point(Point):
    a = 0
    b = 0

    @classmethod
    def __weierstrass(cls, x):
        return (pow(x, 3, cls.prime)
                + cls.a * x % cls.prime
                + cls.b) % cls.prime

    @classmethod
    def recover(cls, primary, bit):
        s = sqrt(cls.__weierstrass(primary), cls.prime)
        assert s != 0

        secondary = s if s & 1 == bit else ((cls.prime - s) % cls.prime)
        return cls(primary, secondary)

    def __init__(self, x=None, y=None, z=1):
        assert (x is None and y is None) \
            or (x is not None and y is not None)

        self.__x = 0 if x is None else x
        self.__y = 1 if y is None else y
        self.__z = 0 if y is None else z

    def __normalize(self):
        if self.__z in (0, 1):
            return

        p = self.__class__.prime
        self.__x = self.__x * inv(self.__z, p) % p
        self.__y = self.__y * inv(self.__z, p) % p
        self.__z = 1

    @property
    def is_identity(self):
        return self.__z == 0

    @property
    def is_valid(self):
        if self.is_identity:
            return False

        l = self.__class__.__weierstrass(self.x)
        r = self.y * self.y % self.__class__.prime
        return l == r

    @property
    def x(self):
        self.__normalize()
        return self.__x if self.__z == 1 else None

    @property
    def y(self):
        self.__normalize()
        return self.__y if self.__z == 1 else None

    def __add__(self, other):
        assert isinstance(other, self.__class__)

        p = self.__class__.prime

        if self.is_identity or other.is_identity:
            return self if other.is_identity else other

        u = (other.__y * self.__z % p - self.__y * other.__z % p) % p
        v = (other.__x * self.__z % p - self.__x * other.__z % p) % p

        if u != 0 and v == 0:
            X3 = 0
            Y3 = 1
            Z3 = 0

        elif u == 0 and v == 0:
            XX = self.__x * self.__x % p
            YY = self.__y * self.__y % p
            ZZ = self.__z * self.__z % p
            YZ = self.__y * self.__z % p
            YYZ = YY * self.__z % p

            w = (3 * XX % p + self.__class__.a * ZZ % p) % p
            ww = w * w % p
            www = w * ww % p

            X3 = (ww - 8 * self.__x % p * YYZ % p) % p
            X3 = 2 * YZ % p * X3 % p
            Y3 = (3 * w % p * self.__x % p - 2 * YYZ % p) % p
            Y3 = (4 * YYZ % p * Y3 % p - www) % p
            Z3 = 8 * YYZ % p * ZZ % p * self.__y % p

        else:
            uu = u * u % p
            uuu = u * uu % p
            vv = v * v % p
            vvv = v * vv % p

            X1vv = self.__x * vv % p

            X3 = (self.__z * uu % p - 2 * X1vv % p) % p
            X3 = v * ((other.__z * X3 % p - vvv) % p) % p
            Y3 = 3 * u % p * X1vv % p
            Y3 = ((Y3 - self.__y * vvv % p) % p - self.__z * uuu % p) % p
            Y3 = (other.__z * Y3 % p + u * vvv % p) % p
            Z3 = vvv * self.__z % p * other.__z % p

        return self.__class__(X3, Y3, Z3)

    def __eq__(self, other):
        p = self.__class__.prime
        x = other.__x * self.__z % p == self.__x * other.__z % p
        y = other.__y * self.__z % p == self.__y * other.__z % p
        return x and y
