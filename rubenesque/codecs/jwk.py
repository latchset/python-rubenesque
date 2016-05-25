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

from ..lcodec import lenc, ldec
from ..curves import find
import base64

def b64u_enc(x):
    return base64.b64encode(x, b"-_").decode("UTF-8").rstrip("=")

def b64u_dec(x):
    x += "=" * (4 - len(x) % 4)
    return base64.b64decode(x.encode("UTF-8"), b"-_")

def encode(point, prv=None):
    """Encodes a point to a dictionary representing a JSON Web Token.

    >>> from ..curves.sec import secp256r1
    >>> prv = 95868137618030166809364817078804351319836184172769340930264256928620637034634
    >>> secp256r1.generator() * prv
    secp256r1(808D060082C176EED3E776A4AC598CC8672C1779F974EECC9B03411CA5B9495D, 48B5BFC527DFCE53D6AC7115237D031CCFF87A0570B77350A9E503EE7305A69B)

    >>> jwk = { "kty": "EC", "crv": "P-256"}
    >>> jwk["x"] = "gI0GAILBdu7T53akrFmMyGcsF3n5dO7MmwNBHKW5SV0"
    >>> jwk["y"] = "SLW_xSffzlPWrHEVI30DHM_4egVwt3NQqeUD7nMFpps"
    >>> encode(secp256r1.generator() * prv) == jwk
    True

    >>> jwk["d"] = "0_NxaRPUMQoAJt50Gz8YiTr8gRTwyEaCumd-MToTmIo"
    >>> encode(secp256r1.generator() * prv, prv) == jwk
    True
    """
    assert not point.is_identity

    NAMES = {
        "secp256r1": "P-256",
        "secp384r1": "P-384",
        "secp521r1": "P-521",
    }

    x = lenc(point.x, (point.bits() + 7) // 8)
    y = lenc(point.y, (point.bits() + 7) // 8)

    jwk = {
        "kty": "EC",
        "crv": NAMES.get(point.__class__.__name__, point.__class__.__name__),
        "x": b64u_enc(x),
        "y": b64u_enc(y),
    }

    if prv is not None:
        d = lenc(prv, (point.bits() + 7) // 8)
        jwk["d"] = b64u_enc(d)

    return jwk


def decode(jwk):
    """Decodes a JSON Web Token to a Point and a private key.

    >>> jwk = { "kty": "EC", "crv": "P-256"}
    >>> jwk["x"] = "gI0GAILBdu7T53akrFmMyGcsF3n5dO7MmwNBHKW5SV0"
    >>> jwk["y"] = "SLW_xSffzlPWrHEVI30DHM_4egVwt3NQqeUD7nMFpps"
    >>> pub, prv = decode(jwk)
    >>> prv is None
    True
    >>> pub
    secp256r1(808D060082C176EED3E776A4AC598CC8672C1779F974EECC9B03411CA5B9495D, 48B5BFC527DFCE53D6AC7115237D031CCFF87A0570B77350A9E503EE7305A69B)

    >>> jwk["d"] = "0_NxaRPUMQoAJt50Gz8YiTr8gRTwyEaCumd-MToTmIo"
    >>> pub, prv = decode(jwk)
    >>> prv == 95868137618030166809364817078804351319836184172769340930264256928620637034634
    True
    >>> pub
    secp256r1(808D060082C176EED3E776A4AC598CC8672C1779F974EECC9B03411CA5B9495D, 48B5BFC527DFCE53D6AC7115237D031CCFF87A0570B77350A9E503EE7305A69B)
    """
    assert jwk["kty"] == "EC"

    crv = find(jwk["crv"])
    x = ldec(b64u_dec(jwk["x"]))
    y = ldec(b64u_dec(jwk["y"]))
    d = jwk.get("d", None)

    if d is not None:
        d = ldec(b64u_dec(d))

    return (crv(x, y), d)
