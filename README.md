pidtoolkit — generate PIDs for Flemish Museums
==============================================

## Description
pidtoolkit is a python toolkit for the generation of PIDs for museum objects, based on the current practice in Flemish museums. Extra fields are generated according to the practice in museums using Adlib via ErfgoedInZicht. These may not be necessary or relevant for other collection management systems.

**Note: the current version was created for use with the Flemish Art Collection's data and image aggregation infrastructure. As such naming and functionality reflects this.**

## Changelog
### v0.1b
- Split into multiple files
- Disabled representation redirects for CultURIze generation due to incompatibility with the Flemish Art Collection's IIIF infrastructure

### v0.1a
Initial version.

## Usage

```
python pidtoolkit [-h] -c CONFIG [-d DEST] [-u {true,false}] csv

positional arguments:
  csv                   Path to CSV file with object numbers

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to generation configuration file. Required.
  -d DEST, --dest DEST  Path to destination directory
  -u {true,false}, --urls {true,false}
                        Generate CSV with URLs for CultURIze. Default 'true'.
```

The generation of PIDs is governed by the options set in the configuration file. See `src/config` for an example file with explanations.