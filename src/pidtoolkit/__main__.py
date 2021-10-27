#!/usr/bin/env python

from argparse import ArgumentParser
from os import path

from pids.csvgen import generate_pid_csv


def main(args):
    import_file = args.csv
    export_file = args.dest if args.dest else path.dirname(path.realpath(import_file)) + 'pids.csv'
    config_file = args.config

    generate_pid_csv(import_file, export_file, config_file)
    print("PIDs exported to:", export_file)

    print("Finished.")


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate PIDs from object numbers")
    parser.add_argument('csv', help="Path to CSV file with object numbers")
    parser.add_argument('-c', '--config', required=True,
                        help="Path to generation configuration file. Required.")
    parser.add_argument('-d', '--dest',
                        help="Path to destination file")
    args = parser.parse_args()
    main(args)
