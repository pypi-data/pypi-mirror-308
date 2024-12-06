# Copyright © 2012-2024 Jakub Wilk <jwilk@jwilk.net>
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
XMP support (GExiv2 backend)
"""

import re

# noinspection PyUnresolvedReferences
import gi
try:
    gi.require_version('GExiv2', '0.10')
except ValueError as exception:  # no coverage
    raise ImportError(exception)
# noinspection PyUnresolvedReferences
from gi.repository import GExiv2
if GExiv2.get_version() < 1202:
    # Version format: https://valadoc.org/gexiv2/GExiv2.get_version.html
    raise ImportError('GExiv2 >= 0.12.2 is required')  # no coverage

from didjvu import temporary
from didjvu import timestamp

from didjvu.xmp import namespaces


try:
    GExiv2.Metadata.try_register_xmp_namespace(namespaces.didjvu, 'didjvu')
except AttributeError:  # no coverage
    # GEXiv2 < 0.14.0
    # Might be dropped in April 2025 when Ubuntu 20.04 is EOL.
    GExiv2.Metadata.register_xmp_namespace(namespaces.didjvu, 'didjvu')


def _get_versions():
    yield f'PyGI {gi.__version__}'
    version_int = GExiv2.get_version()
    major_minor, patch = divmod(version_int, 100)
    major, minor = divmod(major_minor, 100)
    yield f'GExiv2 {major}.{minor}.{patch}'


versions = list(_get_versions())


class XmpError(RuntimeError):
    pass


class MetadataBase:
    _empty_xmp = (
        f'<x:xmpmeta xmlns:x="adobe:ns:meta/" xmlns:rdf="{namespaces.rdf}">'
        f'<rdf:RDF/>'
        f'</x:xmpmeta>'
    )

    def _read_data(self, data):
        fp = temporary.file(suffix='.xmp')
        try:
            fp.write(data.encode('utf-8'))
            fp.flush()
            self._meta = GExiv2.Metadata()
            self._meta.open_path(fp.name)
        finally:
            fp.close()

    def __init__(self):
        self._read_data(self._empty_xmp)

    def get(self, key, fallback=None):
        try:
            return self[key]
        except LookupError:
            return fallback

    def __getitem__(self, key):
        value = self._meta.try_get_tag_string(f'Xmp.{key}')
        if value is None:
            raise KeyError(f'Xmp.{key}')
        return value

    def __setitem__(self, key, value):
        if isinstance(value, timestamp.Timestamp):
            value = str(value)
        elif key.startswith('didjvu.'):
            value = str(value)
        self._meta.try_set_tag_string(f'Xmp.{key}', value)

    def _add_to_history(self, event, index):
        for key, value in event.items:
            if value is None:
                continue
            self[f'xmpMM.History[{index}]/stEvt:{key}'] = value

    def append_to_history(self, event):
        regexp = re.compile(r'^Xmp[.]xmpMM[.]History\[(\d+)\]/')
        n = 0
        for key in self._meta.get_xmp_tags():
            match = regexp.match(key)
            if match is None:
                continue
            i = int(match.group(1))
            n = max(i, n)
        if n == 0:
            self._meta.try_set_xmp_tag_struct('Xmp.xmpMM.History', GExiv2.StructureType.SEQ)
        return self._add_to_history(event, n + 1)

    def serialize(self):
        return '<?xml version="1.0"?>\n' + (
            self._meta.try_generate_xmp_packet(
                GExiv2.XmpFormatFlags.OMIT_PACKET_WRAPPER,
                0
            ) or self._empty_xmp
        )

    def read(self, fp):
        data = fp.read()
        self._read_data(data)


__all__ = [
    'MetadataBase',
    'versions',
]
