import unittest
from oseg import parser


class TestNormalizeStr(unittest.TestCase):
    def test_underscore(self):
        data = {
            "A": "A",
            "a": "a",
            "Ab": "Ab",
            "AB": "A_B",
            "aB": "a_B",
            "OAuthName": "O_Auth_Name",
            "abcdefg123hij456": "abcdefg123hij456",
            "Abcdefg123hij456": "Abcdefg123hij456",
            "ABcdefg123hij456": "A_Bcdefg123hij456",
            "ABCdefg123hij456": "A_B_Cdefg123hij456",
            "ABCDefg123hij456": "A_BC_Defg123hij456",
            "ABCDEfg123hij456": "A_BCD_Efg123hij456",
            "ABCDEFg123hij456": "A_BCDEFg123hij456",
            "ABCDEFG123hij456": "A_BCDEFG123hij456",
            "ABCDEFG123Hij456": "A_BCDEFG123_Hij456",
            "ABCDEFG123HIj456": "A_BCDEFG123_HIj456",
            "ABCDEFG123HIJ456": "A_BCDEFG123_HIJ456",
            "ABCDEFG123HiJ456": "A_BCDEFG123_Hi_J456",
            "ABCDEFG123hiJ456": "A_BCDEFG123hi_J456",
            "ABCDEFG123hIJ456": "A_BCDEFG123h_IJ456",
            "aBcdefg123hij456": "a_Bcdefg123hij456",
            "aBCdefg123hij456": "a_B_Cdefg123hij456",
            "aBCDefg123hij456": "a_BC_Defg123hij456",
            "aBCDEfg123hij456": "a_BCD_Efg123hij456",
            "aBCDEFg123hij456": "a_BCDEFg123hij456",
            "aBCDEFG123hij456": "a_BCDEFG123hij456",
            "aBcDeFg123hIj456": "a_Bc_De_Fg123h_Ij456",
        }

        for provided, expected in data.items():
            with self.subTest(provided):
                result = parser.NormalizeStr.underscore(provided)

                self.assertEqual(
                    first=expected,
                    second=result,
                    msg=f"Provided: {provided}, Expected: {expected}, Result: {result}",
                )
