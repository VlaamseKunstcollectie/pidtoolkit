#!/usr/bin/env python

import re


def generate_oslo_ident_pid(inv_number: str, base_url: str, concept: str) -> str:
    """
    Takes an inventory number, the base URL, and the concept and
        generates the identifier PID.
    """

    return re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + "/id/" +
                  concept + inv_number)


def generate_oslo_data_pid(inv_number: str, base_url: str, concept: str) -> str:
    """
    Takes an inventory number, the base URL, and the concept and
        generates the data PID.
    """

    return re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + "/data/" +
                  concept + inv_number)


def generate_oslo_rep_pid(inv_number: str, base_url: str, concept: str) -> str:
    """
    Takes an inventory number, the base URL, and the concept and
        generates the representation PID.
    """

    return re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" +
                  "/representation/" + concept + inv_number)

def generate_oslo_doc_pid(inv_number: str, base_url: str, concept: str) -> str:
    """
    Takes an inventory number, the base URL, and the concept and
        generates the doc PID.
    """

    return re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + "/doc/" +
                  concept + inv_number)