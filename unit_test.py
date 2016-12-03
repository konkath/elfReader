import unittest

from .patcher import get_byte_array


class TestCoderMethods(unittest.TestCase):
    def test_get_byte_array(self):
        # fixed length
        self.assertEqual(get_byte_array("0xffDE8000"), (b'\x00\x80\xde\xff'))
        self.assertEqual(get_byte_array("0xff"), (b'\xff'))
        self.assertEqual(get_byte_array("0xffaB"), (b'\xab\xff'))

        # no 0x
        self.assertEqual(get_byte_array("ffDE8000"), (b'\x00\x80\xde\xff'))
        self.assertEqual(get_byte_array("ff"), (b'\xff'))
        self.assertEqual(get_byte_array("ffaB"), (b'\xab\xff'))

        # weird length
        self.assertEqual(get_byte_array("ffDE801"), (b'\x01\xe8\xfd\x0f'))
        self.assertEqual(get_byte_array("ffDE80"), (b'\x80\xde\xff\00'))
        self.assertEqual(get_byte_array("ffDE8"), (b'\xe8\xfd\x0f\x00'))
        self.assertEqual(get_byte_array("ff0"), (b'\xf0\x0f'))
        self.assertEqual(get_byte_array("f"), (b'\x0f'))

        # excepts
        with self.assertRaises(AttributeError):
            get_byte_array("0x0G3")             # not hex
        with self.assertRaises(AttributeError):
            get_byte_array("0x00000000F")       # too long
        with self.assertRaises(AttributeError):
            get_byte_array("")                  # empty string
