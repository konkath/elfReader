import sys
from elftools.elf.elffile import ELFFile


# FA = S_FA + ( VA – S_VA)
# VA = podajemy
# S_VA – poczatek sekcji (Addr)
# S_FA – adres sekcji w pliku (OFF)


def process_file(filename):
    with open(filename, 'rb') as f:
        elf_file = ELFFile(f)

        if not elf_file.little_endian:
            print('little endian is currently not supported')
            return

        entry_point = elf_file.header['e_entry']
        my_section = None
        s_va = None
        s_fa = None

        for section in elf_file.iter_sections():
            if not section.is_null():
                s_va = section.header['sh_addr']
                s_fa = section.header['sh_offset']
                s_end = s_va + s_fa

                print(s_va, entry_point, s_end)

                if s_va < entry_point < s_end:
                    my_section = section
                    break

        if my_section:
            va = int(sys.argv[2], 16)
            print(s_va, s_fa, va)
            fa = s_fa + (va - s_va)
            print(fa)

            f.seek(fa)
            print(f.read(4))


process_file(sys.argv[1])
