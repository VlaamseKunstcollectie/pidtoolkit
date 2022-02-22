#!/usr/bin/env python

import csv
import json
from datetime import date

from pids.pidgen import replace_unsafe_chars, generate_meemoo_pid, generate_oslo_pid


def generate_pid_csv(import_file: str, export_file: str, config_file: str):
    # Import configuration from JSON file
    json_file = open(config_file,)
    config = json.load(json_file)

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
    include_websafe_number = config['include_websafe_number']
    historic_adlib_ei = config['historic_adlib_ei']

    if historic_adlib_ei:
        inst_from_field = config['institution_field']
        institution_field = config['institution']
        inst_has_divisions = config['department_field']
        division_field = config['department']

    # Import CSV file with object numbers and optional extra information
    csv_contents = csv.DictReader(open(import_file, encoding=file_encoding))

    # Make and export row-by-row a CSV file with PIDs
    with open(export_file, 'w') as output_file:
        # define list of field names for the header row
        fields = []
        if has_priref:
            fields.append("record_number")
        fields.append("object_number")
        if include_websafe_number:
            fields.append("websafe_obj_number")
        if historic_adlib_ei:
            fields.append("date")
            fields.append("institution")
        for type in pid_types:
            fields.append(f"{type}_pid")
            fields.append(f"{type}_pid.type")

        # define dictionary of field-value pairs for the content rows
        export_row = {}
        if has_priref:
            export_row['record_number'] = ""
        export_row["object_number"] = ""
        if include_websafe_number:
            export_row["websafe_obj_number"] = ""
        if historic_adlib_ei:
            export_row["date"] = ""
            export_row["institution"] = ""
        for type in pid_types:
            export_row[f"{type}_pid"] = ""
            export_row[f"{type}_pid.type"] = ""

        # create the CSV file with header row
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()

        # create the content rows
        for import_row in csv_contents:
            pid_number = replace_unsafe_chars(import_row[obj_number_field])

            if has_priref:
                export_row["record_number"] = import_row[priref_field]

            export_row["object_number"] = import_row[obj_number_field]

            if include_websafe_number:
                export_row["websafe_obj_number"] = pid_number

            if historic_adlib_ei:
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
                    export_row[f"{type}_pid.type"] = f"{type}pid"
            else:
                for type in pid_types:
                    export_row[f"{type}_pid"] = generate_meemoo_pid(pid_number, base_url, pid_concept, type, pid_pattern)
                    export_row[f"{type}_pid.type"] = f"{type}pid"

            writer.writerow(export_row)
