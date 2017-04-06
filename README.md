Rubenesque
==========

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
```
>>> from rubenesque.codecs.sec import encode, decode
>>> import rubenesque.curves
>>> secp256r1 = rubenesque.curves.by_name('secp256r1')
```

Alice generates her private and public keys:
```
>>> alice_prv = secp256r1.private_key()
>>> alice_pub = secp256r1.generator() * alice_prv
>>> alice_enc = encode(alice_pub)
```

Bob does the same:
```
>>> bob_prv = secp256r1.private_key()
>>> bob_pub = secp256r1.generator() * bob_prv
>>> bob_enc = encode(bob_pub)
```
After exchanging their encoded keys, Alice computes the session key:
```
>>> alice_ses = decode(secp256r1, bob_enc) * alice_prv
```

Bob does the same:
```
>>> bob_ses = decode(secp256r1, alice_enc) * bob_prv
```

Notice that Bob and Alice share the same session key, but not private key:
```
>>> alice_prv == bob_prv
False
>>> alice_ses == bob_ses
True
```


License
========
Rubenesque is licensed under the BSD 2-Clause license.
