#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
The main application body for ELFReader.
"""

# pylint: disable=relative-beyond-top-level

import sys
import errno
from argparse import ArgumentParser
from os import R_OK, access
from os.path import isfile

from elftools.elf.elffile import ELFFile
from tabulate import tabulate

from elfreader.elfparser import get_executable_sections


def prepare_parser() -> ArgumentParser:
    """Prepare and configure the argument parser.

    Returns:
        A configured argument parser.
    """
    argparser = ArgumentParser(
        prog="ELFReader",
        description="Program for printing all the executable segments of an ELF file.",
    )
    argparser.add_argument("filename", help="The path to the ELF file.")
    argparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="If set, print the entire contents of each executable section.",
    )
    return argparser


def main(filepath: str, verbose: bool = False) -> None:
    """The main application loop.

    Args:
        filepath (str): The path to the ELF file.
        verbose (bool): Whether to print contents of the found sections.
    """

    # Checking the file validity
    if not isfile(filepath):
        print("The supplied path is not a valid file. Exiting.")
        sys.exit(errno.ENOENT)

    if not access(filepath, R_OK):
        print("Insufficient permissions to read the given file. Exiting.")
        sys.exit(errno.EPERM)

    # Loading the file
    try:
        elffile = ELFFile.load_from_path(filepath)
    except (OSError, IOError) as err:
        print(f"Unable to open the ELF file. {err}")
        sys.exit(errno.EIO)
    except Exception as err:  # pylint: disable=broad-except
        print(f"Exception encountered when reading the ELf file. {err}")
        sys.exit(999)

    # Getting the executable sections
    sections = get_executable_sections(elffile)
    print(f"Found {len(sections)} sections with executable code.")

    if len(sections) == 0:
        sys.exit(0)

    # Printing them to stdout
    if not verbose:
        header = ["section"] + list(sections[0].header.keys())
        values = [[s.name] + list(dict(s.header).values()) for s in sections]
        print(tabulate(values, header, tablefmt="simple_outline"))
    else:
        for sec in sections:
            print("─" * 30)
            print(f"Name: {sec.name}")
            print("Header:")
            for key, val in dict(sec.header).items():
                print(f"\t{key}: {val}")
            print("Contents:")
            print(f"\t{sec.data()}")


if __name__ == "__main__":
    # Get the arguments
    parser = prepare_parser()
    args = parser.parse_args()

    # Run the application
    main(args.filename, args.verbose)
