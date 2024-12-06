# Copyright © 2009-2015 Jakub Wilk <jwilk@jwilk.net>
# Copyright © 2022-2024 FriedrichFroebel
#
# This file is part of didjvu.
#
# didjvu is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# didjvu is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.

"""
Temporary files and directories
"""

import contextlib
import functools
import os
import shutil
import tempfile

file = functools.partial(tempfile.NamedTemporaryFile, prefix='didjvu.')
name = functools.partial(tempfile.mktemp, prefix='didjvu.')


# noinspection PyShadowingBuiltins
def hardlink(path, suffix='', prefix='didjvu.', dir=None):
    new_path = name(suffix=suffix, prefix=prefix, dir=dir)
    os.link(path, new_path)
    # noinspection PyUnresolvedReferences,PyProtectedMember
    return tempfile._TemporaryFileWrapper(
        open(new_path, 'r+b'),
        new_path
    )


@contextlib.contextmanager
def directory(*args, **kwargs):
    kwargs = dict(kwargs)
    kwargs.setdefault('prefix', 'didjvu.')
    tmpdir = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


__all__ = [
    'directory',
    'file',
    'hardlink',
    'name',
]
