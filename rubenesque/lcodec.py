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

from binascii import hexlify, unhexlify


if not hasattr(__builtins__, "long"):
    long = int


def lenc(v, l, be=True):
    r"""Encode a long integer to bytes.

    >>> lenc(0xff, 1, True)
    b'\xff'
    >>> lenc(0xff, 1, False)
    b'\xff'
    >>> lenc(0xff, 2, True)
    b'\x00\xff'
    >>> lenc(0xff, 2, False)
    b'\xff\x00'
    """
    fmt = "%%0%dX" % (l * 2)
    v = unhexlify(fmt % v)
    return v if be else v[::-1]


def ldec(v, be=True):
    """Decode a long integer from bytes.

    >>> assert ldec(b'\\xff', True) == 255
    >>> assert ldec(b'\\xff', False) == 255
    >>> assert ldec(b'\\x00\\xff', True) == 255
    >>> assert ldec(b'\\x00\\xff', False) == 65280
    """
    return long(hexlify(v if be else v[::-1]), 16)
