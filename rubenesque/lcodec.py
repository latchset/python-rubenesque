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

from __future__ import absolute_import
import sys

if sys.version_info >= (3,):
    def lenc(v, l, be=True):
        """Encode a long integer to a bytearray.

        >>> lenc(0xff, 1, True)
        b'\\xff'
        >>> lenc(0xff, 1, False)
        b'\\xff'
        >>> lenc(0xff, 2, True)
        b'\\x00\\xff'
        >>> lenc(0xff, 2, False)
        b'\\xff\\x00'
        """
        return v.to_bytes(l, 'big' if be else 'little')


    def ldec(v, be=True):
        """Decode a long integer from bytes.

        >>> ldec(b'\\xff', True)
        255
        >>> ldec(b'\\xff', False)
        255
        >>> ldec(b'\\x00\\xff', True)
        255
        >>> ldec(b'\\x00\\xff', False)
        65280
        """
        return int.from_bytes(v, 'big' if be else 'little')
else:
    import codecs


    def lenc(v, l, be=True):
        """Encode a long integer to a bytearray.

        >>> lenc(0xff, 1, True)
        '\\xff'
        >>> lenc(0xff, 1, False)
        '\\xff'
        >>> lenc(0xff, 2, True)
        '\\x00\\xff'
        >>> lenc(0xff, 2, False)
        '\\xff\\x00'
        """
        v = "%X" % v
        if len(v) > l * 2:
            raise OverflowError()
        v = "0" * (l * 2 - len(v)) + v
        return codecs.decode(v if be else bytearray(reversed(v)), 'hex')


    def ldec(v, be=True):
        """Decode a long integer from bytes.

        >>> ldec('\\xff', True)
        255L
        >>> ldec('\\xff', False)
        255L
        >>> ldec('\\x00\\xff', True)
        255L
        >>> ldec('\\x00\\xff', False)
        65280L
        """
        v = codecs.encode(v if be else bytearray(reversed(v)), 'hex')
        return long(v, 16)
