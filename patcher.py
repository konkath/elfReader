import sys
from elftools.elf.elffile import ELFFile


def get_byte_array(my_byte):
    if len(my_byte) > 10:
        print('Wrong byte length provided - stopping!')
        raise AttributeError

    try:
        int(my_byte, 16)
    except ValueError:
        print('Wrong byte provided - stopping!')
        raise AttributeError

    if '0x' in my_byte:
        my_byte = my_byte.replace('0x', '')

    # Strings lengths are number of bytes * 2
    while len(my_byte) != 2 and len(my_byte) != 4 and len(my_byte) != 8:
        my_byte = '0' + my_byte[0:]

    n = 2
    byte_arr = bytearray([int(my_byte[i:i + n], 16) for i in range(0, len(my_byte), n)])
    return byte_arr[::-1]


def process_file(filename):
    with open(filename, 'r+b') as f:
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

                if s_va < entry_point < s_end:
                    my_section = section
                    break

        if my_section:
            va = int(sys.argv[2], 16)
            fa = s_fa + (va - s_va)

            for my_byte in sys.argv[3:]:
                try:
                    get_byte_array(my_byte)
                    my_byte_array = get_byte_array(my_byte)
                    print(my_byte_array)
                except AttributeError:
                    return

if __name__ == '__main__':
    process_file(sys.argv[1])
