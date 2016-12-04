import sys
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError


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


def get_addresses(elf_file):
    entry_point = elf_file.header['e_entry']

    for section in elf_file.iter_sections():
        if not section.is_null():
            s_va = section.header['sh_addr']
            s_fa = section.header['sh_offset']
            s_end = s_va + s_fa

            if s_va < entry_point < s_end:
                return s_va, s_fa
    return None


def write_to_file(file, fa, my_byte_array):
    file.seek(fa)
    file_bytes = file.read(len(my_byte_array))

    if len(file_bytes) != len(my_byte_array):
        print('EOF reached - stopping!')
        raise EOFError

    file.seek(fa)
    file.write(my_byte_array)


def process_file(filename):
    with open(filename, 'r+b') as file:
        try:
            elf_file = ELFFile(file)
        except ELFError:
            print('This is not elf binary file - stopping!')
            return

        if not elf_file.little_endian:
            print('little endian is currently not supported')
            return

        s_va, s_fa = get_addresses(elf_file)
        if s_va and s_fa:
            try:
                va = int(sys.argv[2], 16)
            except ValueError:
                print('Wrong address provided - stopping!')
                return

            fa = s_fa + (va - s_va)
            for my_byte in sys.argv[3:]:
                try:
                    my_byte_array = get_byte_array(my_byte)
                    write_to_file(file, fa, my_byte_array)
                    fa += len(my_byte_array)
                except AttributeError:
                    return
                except EOFError:
                    return

            print('Swapping operation completed with success!')
        else:
            print('Invalid section!')


if __name__ == '__main__':
    process_file(sys.argv[1])
