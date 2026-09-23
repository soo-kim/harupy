"""Korean text helpers."""

from functools import wraps
from unicodedata import normalize


_DIGITS = ('', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구')
_SMALL_UNITS = ('', '십', '백', '천')
_LARGE_UNITS = ('', '만', '억', '조', '경', '해', '자', '양', '구', '간', '정', '재', '극')
_NUMBER_WORDS = frozenset(_DIGITS[1:] + _SMALL_UNITS[1:] + _LARGE_UNITS[1:] + ('영', '공'))

_JONGSEONG = (
    '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
    'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
)

_JOSA = ('으로', '로', '이', '가', '은', '는', '을', '를', '과', '와', '아', '야')


class String(str):
    """A :class:`str` subclass with helpers for Korean text."""

    def __new__(cls, value):
        return super().__new__(cls, value)

    def __add__(self, other):
        return String(super().__add__(other))

    def __radd__(self, other):
        return String(other.__add__(self))

    def __mul__(self, other):
        return String(super().__mul__(other))

    def __rmul__(self, other):
        return String(super().__rmul__(other))

    def __getitem__(self, item):
        return String(super().__getitem__(item))

    def __iter__(self):
        for character in self.__str__():
            yield String(character)

    def __getattribute__(self, name):
        # ``String('오솔길').로`` is shorthand for ``String('오솔길').josa('로')``.
        if name and all('\uac00' <= character <= '\ud7a3' for character in name):
            return self.josa(name)

        attribute = super().__getattribute__(name)
        if attribute.__class__.__name__ in ('method', 'builtin_function_or_method'):
            return self._string_result(attribute)
        return attribute

    @staticmethod
    def _string_result(function):
        """Keep string results chainable as ``String`` instances."""

        @wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if type(result) is str:
                return String(result)
            if type(result) is tuple:
                return tuple(String(value) if type(value) is str else value for value in result)
            if type(result) is list:
                return [String(value) if type(value) is str else value for value in result]
            return result

        return wrapper

    def to_hangul(self, read_one=False):
        """Return a decimal integer string written with Korean number words."""

        if not super().isdecimal():
            raise ValueError('Value must be an integer-like string.')

        number = self.__str__().lstrip('0') or '0'
        if number == '0':
            return String('영')
        if number == '1':
            return String(_DIGITS[1])

        chunks = (len(number) + 3) // 4
        if chunks > len(_LARGE_UNITS):
            raise ValueError('Value is too large to read with the supported Korean units.')

        def read_under_10k(value):
            reading = ''
            for position, digit in enumerate(reversed(value)):
                if digit == '0':
                    continue
                spoken_digit = _DIGITS[int(digit)] if digit != '1' or position == 0 or read_one else ''
                reading = spoken_digit + _SMALL_UNITS[position] + reading
            return reading

        reading = ''
        unit_index = 0
        while number:
            number, chunk = number[:-4], number[-4:]
            prefix = read_under_10k(chunk)
            if prefix:
                reading = prefix + _LARGE_UNITS[unit_index] + reading
            unit_index += 1
        return String(reading)

    def to_number(self):
        """Convert Korean number words to an integer."""

        number_string = self.__str__()
        if number_string in ('영', '공'):
            return 0
        if not number_string:
            raise ValueError('Value must not be empty.')

        numbers = []
        for character in number_string:
            if character in _DIGITS:
                numbers.append(_DIGITS.index(character))
            elif character in _SMALL_UNITS:
                unit = 10 ** _SMALL_UNITS.index(character)
                if numbers and numbers[-1] < 10:
                    numbers[-1] *= unit
                else:
                    numbers.append(unit)
            elif character in _LARGE_UNITS:
                under_10k = 0
                while numbers and numbers[-1] < 10000:
                    under_10k += numbers.pop()
                numbers.append((under_10k or 1) * (10000 ** _LARGE_UNITS.index(character)))
            else:
                raise ValueError(f'{character} is invalid. It must be a Korean number word.')
        return sum(numbers)

    def isnumeric(self):
        """Also recognize numbers written with Korean number words."""

        return super().isnumeric() or (bool(self) and all(character in _NUMBER_WORDS for character in self))

    def hangul_rate(self):
        """Return the percentage of Hangul characters in the string."""

        if not self:
            return 0
        hangul_count = sum(
            1 for character in self
            if '\uac00' <= character <= '\ud7a3' or '\u3131' <= character <= '\u3163'
        )
        return int(hangul_count * 100 / len(self))

    def extract_readable(self, only_hangul=False):
        """Keep characters whose pronunciation is understood by ``get_last_bachim``."""

        readable = ''
        for character in self:
            if '\uac00' <= character <= '\ud7a3':
                readable += character
            elif only_hangul is False and (
                '\u3131' <= character <= '\u3163' or character.isascii() and character.isalnum()
            ):
                readable += character
        return String(readable)

    def get_last_bachim(self):
        """Return the final consonant used to choose a Korean postposition."""

        readable = self.extract_readable()
        if not readable:
            return None

        character = readable[-1]
        if character.isascii() and character.isdigit():
            return ('ㅇ', 'ㄹ', '', 'ㅁ', '', '', 'ㄱ', 'ㄹ', 'ㄹ', '')[int(character)]
        if 'A' <= character <= 'Z':
            return (
                '', '', '', '', '', '', '', '', '', '', '', 'ㄹ', 'ㅁ', 'ㄴ', '', '', '', 'ㄹ',
                '', '', '', '', '', '', '', '',
            )[ord(character) - ord('A')]
        if 'a' <= character <= 'z':
            return (
                '', 'ㅂ', 'ㄱ', '', '', '', 'ㄱ', '', '', '', 'ㄱ', 'ㄹ', 'ㅁ', 'ㄴ', '', 'ㅂ', '', '',
                '', '', '', '', '', '', '', '',
            )[ord(character) - ord('a')]
        if '\uac00' <= character <= '\ud7a3':
            return _JONGSEONG[(ord(character) - ord('가')) % 28]
        if '\u3131' <= character <= '\u314e':
            return (
                'ㄱ', 'ㄱ', 'ㅅ', 'ㄴ', 'ㅈ', 'ㅎ', 'ㄷ', 'ㄷ', 'ㄹ', 'ㄱ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅌ', 'ㅍ',
                'ㅎ', 'ㅁ', 'ㅂ', 'ㅂ', 'ㅅ', 'ㅅ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
            )[ord(character) - ord('ㄱ')]
        if '\u314f' <= character <= '\u3163':
            return ''
        return None

    def josa(self, postposition):
        """Append the appropriate Korean postposition for the last sound."""

        if not isinstance(postposition, str):
            raise ValueError('Josa must be a string.')
        if not self:
            raise ValueError('String value must not be empty.')

        if postposition not in _JOSA:
            infix = '이' if self.get_last_bachim() else ''
            return String(self + infix + postposition.lstrip('이'))

        pair_index = (_JOSA.index(postposition) // 2) * 2
        bachim = self.get_last_bachim()
        if pair_index == 0:
            selected = 1 if not bachim or bachim == 'ㄹ' else 0
        else:
            selected = 0 if bachim else 1
        return String(self + _JOSA[pair_index + selected])

    def normalize(self, form='NFKD'):
        """Return the Unicode-normalized string."""

        return String(normalize(form, self))
