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


def legendre(n, p):
    """Compute the Legendre Symbol

    >>> legendre(27, 7)
    -1
    >>> legendre(28, 7)
    0
    >>> legendre(29, 7)
    1
    """
    return {0: 0, p - 1: -1}.get(pow(n, (p - 1) // 2, p), 1)


def sqrt(n, p):
    """Compute the square root using Tonelli-Shanks

    >>> sqrt(0, 13)
    0
    >>> sqrt(1, 13)
    1
    >>> sqrt(2, 13)
    0
    >>> sqrt(3, 13)
    9
    >>> sqrt(4, 13)
    11
    >>> sqrt(5, 13)
    0
    >>> sqrt(6, 13)
    0
    >>> sqrt(7, 13)
    0
    >>> sqrt(8, 13)
    0
    >>> sqrt(9, 13)
    3
    >>> sqrt(10, 13)
    7
    >>> sqrt(11, 13)
    0
    >>> sqrt(12, 13)
    8
    """
    if legendre(n, p) != 1:
        return 0
    if n == 0:
        return 0
    if p == 2:
        return n

    s = 0
    q = p - 1
    while q & 1 == 0:
        q >>= 1
        s += 1

    if s == 1:
        return pow(n, (p + 1) // 4, p)

    z = 2
    while legendre(z, p) != -1:
        z += 1

    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    c = pow(z, q, p)
    m = s

    while True:
        if t == 1:
            return r
        for i in range(m):
            if pow(t, 2 ** i, p) == 1:
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                break

    assert False


def egcd(a, b):
    """
    >>> egcd(3, 7)
    (1, -2, 1)
    """
    if a == 0:
        return (b, 0, 1)

    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)


def inv(n, m):
    """Calculate the multiplicitive inverse

    >>> inv(7, 13)
    2
    """
    g, x, y = egcd(n, m)
    return x % m if g == 1 else None
