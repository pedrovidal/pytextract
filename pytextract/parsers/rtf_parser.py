from striprtf.striprtf import rtf_to_text

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from rtf files using striprtf."""

    def extract(self, filename, **kwargs):
        with open(filename) as stream:
            rtf = stream.read()
        return rtf_to_text(rtf)
