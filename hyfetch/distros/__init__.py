from __future__ import annotations

import re
import string
from pathlib import Path

RE_NEOFETCH_COLOR = re.compile('\\${c[0-9]}')


def _ascii_size(asc: str) -> tuple[int, int]:
    """
    Get distro ascii width, height ignoring color code

    :param asc: Distro ascii
    :return: Width, Height
    """
    return max(len(line) for line in re.sub(RE_NEOFETCH_COLOR, '', asc).split('\n')), len(asc.split('\n'))


class AsciiArt:
    name: str
    match: str
    color: str
    ascii: str

    def __init__(self, match: str, color: str, ascii: str, name: str | None = None):
        self.match = match
        self.color = color
        self.ascii = ascii
        self.name = name or self.get_friendly_name()

    @classmethod
    def from_neofetch_output(cls, color: str, ascii: str, distro: str) -> cls:
        return cls(match='NotAvailable', color=color, ascii=ascii, name=distro)

    @classmethod
    def from_ascii_only(cls, ascii: str) -> cls:
        return cls(match='NotAvailable', color='', ascii=ascii, name='Custom')

    def get_friendly_name(self) -> str:
        return self.match.split("|")[0].strip(string.punctuation + '* ') \
            .replace('"', '').replace('*', '')

    def normalized_ascii(self) -> str:
        """
        Make sure every line are the same width
        """
        w = _ascii_size(self.ascii)[0]
        return '\n'.join(line + ' ' * (w - _ascii_size(line)[0]) for line in self.ascii.split('\n'))

    def size(self) -> tuple[int, int]:
        return _ascii_size(self.ascii)

    def slots(self) -> set[int]:
        return set(map(int, re.findall('(?<=\\${c)[0-9](?=})', self.ascii)))
