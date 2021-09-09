#!/usr/bin/env python

import configparser
import csv
from datetime import date

from pids.culturize.culturizegen import generate_arthub_pid, generate_datahub_pid, generate_datahub_redirect, \
    generate_data_redirect
from pids.pidgen.general import replace_unsafe_chars, get_number_from_pid, get_source_from_pid
from pids.pidgen.museum import generate_ident_pid, generate_data_pid, generate_rep_pid


def generate_pid_csv(import_file: str, export_file: str, config_file: str):
    config = configparser.ConfigParser()
    config.read(config_file)

    base_url = config.get('PID', 'BASE_URL')
    pid_pattern = config.get('PID', 'PATTERN')

    priref_field = config.get('PID_IMPORT', 'PRIREF')
    obj_number_field = config.get('PID_IMPORT', 'OBJ_NUMBER')
    institution_field = config.get('PID_IMPORT', 'INSTITUTION')
    division_field = config.get('PID_IMPORT', 'DIVISION')
    inst_has_divisions = config.getboolean('PID_IMPORT', 'INST_DIVISIONS')
    inst_from_field = config.getboolean('PID_IMPORT', 'INST_FROM_FIELD')

    generation_date = date.today().strftime("%Y-%m-%d")

    if not inst_from_field:
        institution = config.get('PID_EXPORT', 'INSTITUTION_NAME')
    else:
        institution = ""

    import_encoding = config.get('PID_IMPORT', 'ENCODING')

    csv_contents = csv.DictReader(open(import_file, encoding=import_encoding))

    with open(export_file, 'w') as output_file:
        fields = [
            "priref",
            "object_number",
            "websafe_obj_number",
            "date",
            "institution",
            "ident_pid",
            "ident_pid.type",
            "data_pid",
            "data_pid.type",
            "rep_pid",
            "rep_pid.type"
        ]
        export_row = {
            "priref": "",
            "object_number": "",
            "websafe_obj_number": "",
            "date": generation_date,
            "institution": institution,
            "ident_pid": "",
            "ident_pid.type": "identifierpid",
            "data_pid": "",
            "data_pid.type": "datapid",
            "rep_pid": "",
            "rep_pid.type": "representationpid"
        }
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()
        for import_row in csv_contents:
            pid_number = replace_unsafe_chars(import_row[obj_number_field])

            export_row["priref"] = import_row[priref_field]
            export_row["object_number"] = import_row[obj_number_field]
            export_row["websafe_obj_number"] = pid_number
            export_row["ident_pid"] = generate_ident_pid(pid_number, base_url,
                                                         pid_pattern)
            export_row["data_pid"] = generate_data_pid(pid_number, base_url,
                                                       pid_pattern)
            export_row["rep_pid"] = generate_rep_pid(pid_number, base_url,
                                                     pid_pattern)

            if inst_from_field and inst_has_divisions:
                export_row["institution"] = import_row[institution_field] \
                                            + " - " + import_row[division_field]
            elif inst_from_field:
                export_row["institution"] = import_row[institution_field]

            writer.writerow(export_row)


def generate_culturize_csv(import_file: str, export_file: str, config_file: str):
    config = configparser.ConfigParser()
    config.read(config_file)

    arthub_url = config.get('URL', 'ARTHUB_URL')
    arthub_lang = config.get('URL', 'ARTHUB_LANG')
    datahub_url = config.get('URL', 'DATAHUB_URL')

    has_pid_field = config.getboolean('CULTURIZE_IMPORT', 'HAS_FIELD')
    pid_field = config.get('CULTURIZE_IMPORT', 'PID_NUMBER')
    ident_pid_field = config.get('CULTURIZE_IMPORT', 'IDENT_PID')
    data_pid_field = config.get('CULTURIZE_IMPORT', 'DATA_PID')
    import_encoding = config.get('CULTURIZE_IMPORT', 'ENCODING')

    data_to_datahub = config.getboolean('CULTURIZE_EXPORT', 'DATA_TO_DATAHUB')

    csv_contents = csv.DictReader(open(import_file, encoding=import_encoding))

    with open(export_file, 'w') as output_file:
        fields = [
            "PID",
            "URL",
            "document type",
            "enabled"
        ]
        export_row = {
            "PID": "",
            "URL": "",
            "document type": "",
            "enabled": "1"
        }
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()
        for import_row in csv_contents:
            if has_pid_field:
                pid_number = import_row[pid_field]
            else:
                pid_number = get_number_from_pid(import_row[data_pid_field])

            ident_pid_source = get_source_from_pid(import_row[ident_pid_field])
            data_pid_source = get_source_from_pid(import_row[data_pid_field])
            arthub_pid = generate_arthub_pid(pid_number, data_pid_source)
            datahub_pid = generate_datahub_pid(pid_number,
                                               import_row[data_pid_field],
                                               datahub_url)

            export_row["PID"] = pid_number

            if ident_pid_source == data_pid_source:
                export_row["URL"] = import_row[data_pid_field]
                export_row["document type"] = "id"
                writer.writerow(export_row)

            if data_to_datahub:
                export_row["URL"] = generate_datahub_redirect(datahub_url,
                                                              datahub_pid)
            else:
                export_row["URL"] = generate_data_redirect(arthub_url,
                                                           arthub_lang,
                                                           arthub_pid)
            export_row["document type"] = "data"
            writer.writerow(export_row)

            # Generating representation redirects in this manner only works
            # with the non-IIIF Arthub.
            #
            # export_row["URL"] = generate_rep_redirect(arthub_url, arthub_lang,
            #                                           arthub_pid)
            # export_row["document type"] = "representation"
            # writer.writerow(export_row)


def append_rep_redirects(culturize_csv: str, encoding: str):
    csvcontents = csv.DictReader(open(culturize_csv, encoding=encoding))

    with open(culturize_csv, 'a') as output_file:
        fields = [
            "PID",
            "URL",
            "document type",
            "enabled"
        ]
        export_row = {
            "PID": "",
            "URL": "",
            "document type": "",
            "enabled": "1"
        }
        writer = csv.DictWriter(output_file, fieldnames=fields)
        previous_pid = ""
        for import_row in csvcontents:
            if previous_pid == import_row["PID"]:
                continue
            export_row["PID"] = import_row["PID"]
            # TODO: write function to generate the IIIF URLs.
            #  export_row["URL"] =
            export_row["document type"] = "representation"
            writer.writerow(export_row)
            previous_pid = import_row["PID"]