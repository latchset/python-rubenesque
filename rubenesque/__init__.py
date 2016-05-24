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
Rubenesque is an implementation of several standard elliptic curve groups
in pure Python 3 used for cryptographic purposes. The classes contained in
this source code should be sufficient to implement your own cryptographic
primitives.

However, please note that, due to the nature of the Python programming
language, this code cannot guarantee either performance or safety from
side-channel attacks. Using this library in situations where such properties
are required is not advised and may actively lead to security compromise.
Although this project will accept patches to improve performance, we will
not consider performance or side-channel avoidance as valid bugs.

Rubenesque does, however, strive to be correct and standards compliant. This
makes it useful in a variety of scenarios; especially use cases such as
offline cryptography or unit tests against servers programmed in lower level
languages.

Rubenesque is licensed under the BSD 2-Clause license.

Rubenesque currently implements the following curves:
 * brainpoolP160r1
 * brainpoolP192r1
 * brainpoolP224r1
 * brainpoolP256r1
 * brainpoolP320r1
 * brainpoolP384r1
 * brainpoolP512r1
 * edwards25519
 * edwards448
 * MDC201601
 * secp192r1
 * secp224r1
 * secp256r1
 * secp384r1
 * secp521r1

Here is a simple example of doing ECDH with SEC P256 using SEC1 encoding.

Both sides prepare for the exchange by loading the same curve and encoding:
>>> from rubenesque.codecs.sec import encode, decode
>>> import rubenesque.curves
>>> secp256r1 = rubenesque.curves.find('secp256r1')

Alice generates her private and public keys:
>>> alice_prv = secp256r1.private_key()
>>> alice_pub = secp256r1.generator() * alice_prv
>>> alice_enc = encode(alice_pub)

Bob does the same:
>>> bob_prv = secp256r1.private_key()
>>> bob_pub = secp256r1.generator() * bob_prv
>>> bob_enc = encode(bob_pub)

After exchanging their encoded keys, Alice computes the session key:
>>> alice_ses = decode(secp256r1, bob_enc) * alice_prv

Bob does the same:
>>> bob_ses = decode(secp256r1, alice_enc) * bob_prv

Notice that Bob and Alice share the same session key, but not private key:
>>> alice_prv == bob_prv
False
>>> alice_ses == bob_ses
True
"""

