# permanentbis
This is a fork of package [permanent](https://pypi.org/project/permanent/).
First, the fork fixes pointer arithmetics in the C module of this package.
Without this fix, compiling the module for Windows is impossible due to
(defensive) compiler's errors. Second, the fork uses numpy >= 2.0.0, which
introduces an incompatible to previous versions ways of handling complex
numbers in the C interface.

A suggested fix has been proposed as [pull
request](https://github.com/peteshadbolt/permanent/pull/2), and was
recently accepted (to a bit too big extent). The main intention
of this fork is to provide a multiarchitecture packaged distribution on PyPi
and to support numpy 2.x.x.

The remaining part of the readme just repeats the original pacakge description.

# Original description of permanent

Implements Ryser's algorithm for the [permanent](https://en.wikipedia.org/wiki/Permanent).

Install:
```bash
$ pip install permanent
```
Use:
```python
>>> from numpy import *
>>> from permanentbis import permanent
>>> permanent(eye(15, dtype=complex))
(1-0j)
```
