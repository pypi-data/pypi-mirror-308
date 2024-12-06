#!/usr/bin/env python3

from distutils.core import setup, Extension
import numpy

setup(
    ext_modules=[
        Extension(
            'permanentbis', ['./src/permanent.c'],
            extra_compile_args=["-Ofast"],
            include_dirs=[numpy.get_include()]),
    ],
)
