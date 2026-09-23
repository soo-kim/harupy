import unittest

import harupy
from harupy import String
from harupy.text import String as TextString


class PackageTest(unittest.TestCase):
    def test_version_and_public_api(self):
        self.assertEqual(harupy.__version__, '2.0.0')
        self.assertEqual(harupy.VERSION, '2.0.0')
        self.assertIs(harupy.String, String)
        self.assertIs(TextString, String)


class StringBehaviorTest(unittest.TestCase):
    def test_string_operations_preserve_type(self):
        self.assertIsInstance(String('haru').upper(), String)
        self.assertIsInstance(String('haru')[1:], String)
        self.assertIsInstance(String('ha') + 'ru', String)
        self.assertTrue(all(isinstance(value, String) for value in String('a-b').partition('-')))


class JosaTest(unittest.TestCase):
    def test_vowel_and_consonant_endings(self):
        self.assertEqual(String('학교').josa('을'), '학교를')
        self.assertEqual(String('밥').josa('를'), '밥을')
        self.assertEqual(String('게').josa('이나'), '게나')
        self.assertEqual(String('고동').josa('나'), '고동이나')

    def test_rieul_exception_for_ro(self):
        self.assertEqual(String('작심삼일').josa('으로'), '작심삼일로')
        self.assertEqual(String('작전변경').josa('로'), '작전변경으로')

    def test_ascii_endings(self):
        self.assertEqual(String('Ace').josa('가'), 'Ace가')
        self.assertEqual(String('music').josa('가'), 'music이')
        self.assertEqual(String('123').josa('가'), '123이')
        self.assertEqual(String('124').josa('가'), '124가')

    def test_attribute_shorthand(self):
        self.assertEqual(String('오솔길').로, '오솔길로')
        self.assertEqual(String('떡볶이').이나, '떡볶이나')

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            String('').josa('은')
        with self.assertRaises(ValueError):
            String('하루').josa(1)


class NumberTest(unittest.TestCase):
    def test_to_hangul(self):
        cases = {
            0: '영',
            1: '일',
            152000: '십오만이천',
            37501600: '삼천칠백오십만천육백',
            1110000: '백십일만',
        }
        for number, expected in cases.items():
            with self.subTest(number=number):
                self.assertEqual(String(number).to_hangul(), expected)
        self.assertEqual(String('0000').to_hangul(), '영')
        self.assertEqual(String(1110000).to_hangul(read_one=True), '일백일십일만')

    def test_to_number(self):
        cases = {
            '영': 0,
            '공': 0,
            '일': 1,
            '만오천': 15000,
            '천이백십일억천백만': 121111000000,
            '육경사천칠조오백오십만삼백일': 64007000005500301,
        }
        for korean, expected in cases.items():
            with self.subTest(korean=korean):
                self.assertEqual(String(korean).to_number(), expected)

    def test_number_round_trip(self):
        for number in range(10001):
            with self.subTest(number=number):
                self.assertEqual(String(String(number).to_hangul()).to_number(), number)

    def test_invalid_number(self):
        for value in ('', 'one', '일백two'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                String(value).to_number()
        with self.assertRaises(ValueError):
            String('-1').to_hangul()

    def test_isnumeric(self):
        self.assertTrue(String('사천오백만').isnumeric())
        self.assertTrue(String('123').isnumeric())
        self.assertFalse(String('').isnumeric())
        self.assertFalse(String('one').isnumeric())


class HangulHelperTest(unittest.TestCase):
    def test_hangul_rate(self):
        self.assertEqual(String('').hangul_rate(), 0)
        self.assertEqual(String('하루').hangul_rate(), 100)
        self.assertEqual(String('하루ab').hangul_rate(), 50)

    def test_extract_readable(self):
        value = String('하루, Python 3!')
        self.assertEqual(value.extract_readable(), '하루Python3')
        self.assertEqual(value.extract_readable(only_hangul=True), '하루')

    def test_last_bachim(self):
        self.assertEqual(String('밥').get_last_bachim(), 'ㅂ')
        self.assertEqual(String('사과').get_last_bachim(), '')
        self.assertEqual(String('오솔길').get_last_bachim(), 'ㄹ')
        self.assertIsNone(String('!').get_last_bachim())

    def test_normalize(self):
        self.assertEqual(list(String('하루').normalize()), ['ᄒ', 'ᅡ', 'ᄅ', 'ᅮ'])


if __name__ == '__main__':
    unittest.main()
