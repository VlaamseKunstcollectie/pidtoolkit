pidtoolkit — generate PIDs for Flemish Museums
==============================================

## Description
pidtoolkit is a python toolkit for the generation of PIDs for museum objects, using either the syntax for CultURIze or the OSLO standard for persistent URLs.

## Changelog
### v0.2
- Removes CultURIze CSV generation
- Config uses JSON instead of INI
- OSLO-compliant PIDs can now be generated
- Adds config options to exclude record numbers and fields required for Adlib via ErfgoedInzicht

### v0.1b
- Split into multiple files
- Disabled representation redirects for CultURIze generation due to incompatibility with the Flemish Art Collection's IIIF infrastructure

### v0.1a
Initial version.

## Usage

```
usage: pidtoolkit [-h] -c CONFIG [-d DEST] csv

Generate PIDs from object numbers

positional arguments:
  csv                   Path to CSV file with object numbers

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to generation configuration file. Required.
  -d DEST, --dest DEST  Path to destination file


```

The generation of PIDs is governed by the options set in the configuration file. See `src/config` for an example file.