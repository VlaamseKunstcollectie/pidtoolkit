#!/usr/bin/env python

import re
import urllib.parse

import tldextract


def generate_arthub_pid(pid_number: str, data_source: str) -> str:
    """
    Takes a PID number and a PID source and generates an Arthub identifier PID.
    """

    return tldextract.extract(urllib.parse.urlparse(data_source).netloc).domain + ":" + pid_number


def generate_datahub_pid(pid_number: str, data_pid: str, datahub_url: str) -> str:
    """
    Takes a PID number, a data pid and generates a
        Datahub identifier PID.
    """

    datahub_ident = tldextract.extract(urllib.parse.urlparse(data_pid).netloc).domain \
                    + "." + tldextract.extract(urllib.parse.urlparse(data_pid).netloc).suffix
    return "oai:" + urllib.parse.urlparse(datahub_url).netloc + ":" \
           + datahub_ident + ":" + pid_number


def generate_data_redirect(arthub_url: str, arthub_lang: str, arthub_pid: str) -> str:
    """
    Takes the Arthub URL and an Arthub PID and generates the Arthub data
        redirect.
    """
    return re.sub('(?<!ttps:|http:)/{2,}', '/', arthub_url + "/" + arthub_lang +
                  "/catalog/" + arthub_pid)


def generate_datahub_redirect(datahub_url: str, datahub_pid: str) -> str:
    """
    Takes the Datahub URL and a datahub PID and generates the Datahub data
        redirect.
    """
    return re.sub('(?<!ttps:|http:)/{2,}', '/', datahub_url
                  + "/oai/?verb=GetRecord&identifier=" + datahub_pid
                  + "&metadataPrefix=oai_lido")

#TODO: reproduction redirect for IIIF
def generate_rep_redirect(arthub_url: str, arthub_lang: str, arthub_pid: str) -> str:
    """
    Takes the Arthub URL and an Arthub PID and generates the Arthub reproduction
        redirect. This is NOT valid for the IIIF Arthub.
    """
    return re.sub('(?<!ttps:|http:)/{2,}', '/', arthub_url + "/" + arthub_lang
                  + "/iiif/2/" + arthub_pid + "/full/full/0/default.jpg")
