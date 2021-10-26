#!/usr/bin/env python

from argparse import ArgumentParser
from os import path

from pids.csvgen import generate_pid_csv, generate_culturize_csv


def main(args):
    import_file = args.csv
    export_directory = args.dest if args.dest else ''
    pid_export_file = path.join(export_directory, "pids.csv")
    culturize_export_file = path.join(export_directory, "culturize.csv") if args.urls == "true" else ''
    config_file = args.config

    generate_pid_csv(import_file, pid_export_file, config_file)
    print("PIDs exported:", pid_export_file)

    if args.urls == "true":
        generate_culturize_csv(pid_export_file, culturize_export_file, config_file)
        print("CultURIze input CSV generated:", culturize_export_file)

    print("Files generated.")


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate PIDs from object numbers")
    parser.add_argument('csv', help="Path to CSV file with object numbers")
    parser.add_argument('-c', '--config', required=True,
                        help="Path to generation configuration file. Required.")
    parser.add_argument('-d', '--dest',
                        help="Path to destination directory")
    parser.add_argument('-u', '--urls', default="true", choices=['true', 'false'],
                        help="Generate CSV with URLs for CultURIze. Default 'true'.")
    args = parser.parse_args()
    main(args)