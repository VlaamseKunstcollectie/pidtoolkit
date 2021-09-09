#!/usr/bin/env python

import re
import urllib.parse

import tldextract


def replace_unsafe_chars(string: str) -> str:
    """
    Takes a string and replaces the non-alphanumeric, underscore, or hyphen
        characters with an underscore.
    """

    return re.sub('[^0-9a-zA-Z\-_]+', '_', string)


def get_number_from_pid(pid: str) -> str:
    """
    Takes a PID and extracts the PID Number.
    """

    return urllib.parse.urlparse(pid).path.rsplit("/", 1)[-1]

# TODO: Is this needed?
def get_source_from_pid(pid: str) -> str:
    """
    Takes a PID and extracts the source.
    """

    return tldextract.extract(urllib.parse.urlparse(pid).netloc).domain
