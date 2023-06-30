"""
Helper functions for parsing the ELF file.
"""

from typing import List

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import Section
from elftools.elf.constants import SH_FLAGS


def contains_executable(section: Section) -> bool:
    """Check whether the section contains any executable code.

    Sections containing executable code can be identified by the SHF_EXECINSTR (0x4)
    flag in the "sh_flags" section of the header.
    Source: https://en.wikipedia.org/wiki/Executable_and_Linkable_Format#Section_header

    Args:
        section (Section): The section to check.

    Returns:
        True if the section contains executable code, otherwise false.
    """
    # We get the sh_flags section from the header. Since we are accessing a dictionary
    # from an exeternal library, we use the "get" function instead of direct access
    # with a default value of 0.
    flags = section.header.get("sh_flags", 0x0)

    # We do a bitwise AND over the flags using the required EXECINSTR flag, leaving only
    # a single bit active with others being 0. This bit is at the 0x4 position, so it is
    # active if the resulting value is 4.
    return bool((flags & SH_FLAGS.SHF_EXECINSTR) == 4)  # noqa: PLR2004


def get_executable_sections(file: ELFFile) -> List[Section]:
    """Parse the ELF file and return all sections containing executable code.

    Args:
        file (ELFFile): The ELF file to parse.

    Returns:
        A list of all the executable sections.
    """
    sections = []
    for sec in file.iter_sections():
        if contains_executable(sec):
            sections.append(sec)
    return sections
