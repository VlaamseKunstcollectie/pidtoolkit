#!/usr/bin/env python

import csv
from datetime import date
import json

from pidgen import replace_unsafe_chars, generate_meemoo_pid, generate_oslo_pid
from culturize.culturizegen import generate_arthub_pid, generate_datahub_pid, generate_datahub_redirect, \
    generate_data_redirect


def generate_pid_csv(import_file: str, export_file: str, config_file: str):
    # Import configuration from JSON file
    config = json.load(config_file)

    # PID format configuration
    oslo_pids = True if config['syntax'] == "oslo" else False
    pid_types = config['types']
    base_url = config['base_url']
    pid_concept = config['concept']
    pid_pattern = config['path']

    # File configuration
    file_encoding = config['encoding']
    has_priref = config['has_record_numbers']
    priref_field = config['record_numbers']
    obj_number_field = config['object_numbers']
    include_adlib_ei = config['include_adlib_ei']

    if include_adlib_ei:
        inst_from_field = config['institution_field']
        institution_field = config['institution']
        inst_has_divisions = config['department_field']
        division_field = config['department']

    # Import CSV file with object numbers and optional extra information
    csv_contents = csv.DictReader(open(import_file, encoding=file_encoding))

    # Make and export row-by-row a CSV file with PIDs
    with open(export_file, 'w') as output_file:
        # define field names for header row
        fields = []
        if has_priref:
            fields.append("record_number")
        fields.append("object_number")
        fields.append("websafe_obj_number")
        if include_adlib_ei:
            fields.append("date")
            fields.append("institution")
        for type in pid_types:
            fields.append(f"{type}_pid")
            fields.append(f"{type}_pid.type")

        # define dictionary for each content row
        export_row = {}
        if has_priref:
            export_row['record_number'] = ""
        export_row["object_number"] = ""
        export_row["websafe_obj_number"] = ""
        if include_adlib_ei:
            export_row["date"] = ""
            export_row["institution"] = ""
        for type in pid_types:
            export_row[f"{type}_pid"] = ""
            export_row[f"{type}_pid"] = f"{type}pid"

        # create CSV file
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()

        # create content rows
        for import_row in csv_contents:
            pid_number = replace_unsafe_chars(import_row[obj_number_field])

            if has_priref:
                export_row["priref"] = import_row[priref_field]

            export_row["object_number"] = import_row[obj_number_field]
            export_row["websafe_obj_number"] = pid_number

            if include_adlib_ei:
                if inst_from_field and inst_has_divisions:
                    export_row["institution"] = import_row[institution_field] \
                                                            + " - " + import_row[division_field]
                elif inst_from_field:
                    export_row["institution"] = import_row[institution_field]
                else:
                    export_row["institution"] = config['institution_name']

                export_row["date"] = date.today().strftime("%Y-%m-%d")

            if oslo_pids:
                for type in pid_types:
                    export_row[f"{type}_pid"] = generate_oslo_pid(pid_number, base_url, pid_concept, type)
            else:
                for type in pid_types:
                    export_row[f"{type}_pid"] = generate_meemoo_pid(pid_number, base_url, pid_concept, type, pid_pattern)

            writer.writerow(export_row)


# TODO: rewrite for variable PID types
def generate_culturize_csv(import_file: str, export_file: str, config_file: str):
    # Import configuration from JSON file
    config = json.load(config_file)

    # PID-related configuration
    base_url = config['base_url']

    # CultURIze configuration
    arthub_url = config['arthub_url']
    arthub_lang = config['arthub_lang']
    datahub_url = ['datahub_url']
    data_to_datahub = ['data_to_datahub']

    csv_contents = csv.DictReader(open(import_file, encoding='utf-8'))

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
            pid_number = import_row["websafe_obj_number"]

            arthub_pid = generate_arthub_pid(pid_number, base_url)
            datahub_pid = generate_datahub_pid(pid_number, base_url, datahub_url)

            export_row["PID"] = pid_number

            export_row["URL"] = import_row['data_pid']
            export_row["document type"] = "id"
            writer.writerow(export_row)

            if data_to_datahub:
                export_row["URL"] = generate_datahub_redirect(datahub_url, datahub_pid)
            else:
                export_row["URL"] = generate_data_redirect(arthub_url, arthub_lang, arthub_pid)
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
