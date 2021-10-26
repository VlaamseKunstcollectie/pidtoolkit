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


def generate_meemoo_pid(inv_number: str, base_url: str, concept: str, type: str, path: str) -> str:
    """
    Takes an inventory number, the base URL, and the PURL pattern and
        generates the identifier PID.
    """

    return re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + path + "/" + concept + "/" +
                  type + "/" + inv_number)


def generate_oslo_pid(inv_number: str, base_url: str, concept: str, type: str) -> str:
    """
    Takes an inventory number, the base URL, and the concept and
        generates the identifier PID.
    """

    return re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + type + "/" +
                  concept + "/" + inv_number)
