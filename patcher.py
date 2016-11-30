import sys
from elftools.elf.elffile import ELFFile


def process_file(filename):
    with open(filename, 'rb') as f:
        elf_file = ELFFile(f)

        for section in elf_file.iter_sections():
            if not section.is_null():
                print(section.name, format(section.header['sh_addr'], '#x'), format(section.header['sh_offset'], '#x'))


process_file(sys.argv[1])
