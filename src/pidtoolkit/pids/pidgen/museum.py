#!/usr/bin/env python

import re


def generate_ident_pid(inv_number: str, base_url: str, purl_pattern: str) -> str:
    """
    Takes an inventory number, the base URL, and the PURL pattern and
        generates the identifier PID.
    """

    return re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + purl_pattern +
                  "/id/" + inv_number)


def generate_data_pid(inv_number: str, base_url: str, purl_pattern: str) -> str:
    """
    Takes an inventory number, the base URL, and the PURL pattern and
        generates the data PID.
    """

    return re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + purl_pattern +
                  "/data/" + inv_number)


def generate_rep_pid(inv_number: str, base_url: str, purl_pattern: str) -> str:
    """
    Takes an inventory number, the base URL, and the PURL pattern and
        generates the representation PID.
    """

    return re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + purl_pattern +
                  "/representation/" + inv_number)
