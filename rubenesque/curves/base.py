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

import abc
import os

from ..math import inv
from ..lcodec import ldec


if not hasattr(abc, "ABC"):
    abc.ABC = abc.ABCMeta(str('ABC'), (), {})


class Point(abc.ABC):
    generator = None
    cofactor = 1
    aliases = ()
    order = 0

    @classmethod
    @abc.abstractmethod
    def bits(cls):
        "The bit length of points on the curve"

    @classmethod
    @abc.abstractmethod
    def generator(cls):
        "The generator (a.k.a. base point)"

    @classmethod
    def create(cls, primary, secondary):
        "Creates a point using the primary and secondary coordinates"
        return cls(primary, secondary)

    @classmethod
    @abc.abstractmethod
    def recover(cls, primary, bit):
        "Recovers a point using the primary coordinate and a secondary bit"

    @classmethod
    def private_key(cls, min=1):
        "Generates a random integer suitable for use as a private key"
        bytes = (cls.order.bit_length() + 7) // 8
        mask = 2 ** cls.order.bit_length() - 1

        r = 0
        while r < min or r >= cls.order:
            r = ldec(os.urandom(bytes)) & mask

        return r

    @abc.abstractmethod
    def __init__(self, x=None, y=None, *args, **kwargs):
        "Creates a new point with the specified coordinates"

    @abc.abstractproperty
    def is_identity(self):
        "Whether or not this point represents the neutral element"

    @abc.abstractproperty
    def is_valid(self):
        "Whether or not this point represents the neutral element"

    @abc.abstractproperty
    def x(self):
        "The x coordinate"

    @abc.abstractproperty
    def y(self):
        "The y coordinate"

    @property
    def primary(self):
        "The primary coordinate"
        return self.x

    @property
    def secondary(self):
        "The secondary coordinate"
        return self.y

    @abc.abstractmethod
    def __add__(self, other):
        "Adds two points"

    @abc.abstractmethod
    def __eq__(self, other):
        "Tests equality between two points"

    @abc.abstractmethod
    def __neg__(self):
        "Invert a point"

    def __mul__(self, multiplier):
        if multiplier == 0:
            return self.__class__()

        q = self.__class__()
        p = self
        for o in range(multiplier.bit_length(), -1, -1):
            if multiplier & (1 << o):
                q += p
                p += p
            else:
                p += q
                q += q

        return q

    def __div__(self, divisor):
        return self * inv(divisor, self.order)
    __floordiv__ = __div__
    __truediv__ = __div__

    def __sub__(self, other):
        return self + -other

    def __repr__(self):
        if self.is_identity:
            return "%s(∞)" % self.__class__.__name__

        l = (self.__class__.bits() + 7) // 8 * 2
        t = "%s(%%0%dX, %%0%dX)" % (self.__class__.__name__, l, l)
        return t % (self.x, self.y)
