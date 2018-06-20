#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.insert(0, '../')

from harupy.text import String


class TextTest(unittest.TestCase):
	"""
	조사 테스트
	"""
	def test_josa(self):
		self.assertEqual(String('게').josa('나'), '게나')
		self.assertEqual(String('게').josa('이나'), '게나')
		self.assertEqual(String('고동').josa('나'), '고동이나')
		self.assertEqual(String('고동').josa('이나'), '고동이나')
		self.assertEqual(String('학교').josa('을'), '학교를')
		self.assertEqual(String('학교').josa('를'), '학교를')
		self.assertEqual(String('학교').josa('를'), '학교를')
		self.assertEqual(String('Ace').josa('가'), 'Ace가')
		self.assertEqual(String('makers').josa('가'), 'makers가')
		self.assertEqual(String('pop').josa('가'), 'pop이')
		self.assertEqual(String('funky').josa('가'), 'funky가')
		self.assertEqual(String('music').josa('가'), 'music이')
		self.assertEqual(String('JFK').josa('가'), 'JFK가')
		self.assertEqual(String('2PM').josa('가'), '2PM이')
		self.assertEqual(String('1234').josa('가'), '1234가')
		self.assertEqual(String('123').josa('가'), '123이')
		self.assertEqual(String('밥').josa('를'), '밥을')
		self.assertEqual(String('사과').josa('을'), '사과를')
		self.assertEqual(String('명함').josa('을'), '명함을')
		self.assertEqual(String('븅신').josa('다'), '븅신이다')
		self.assertEqual(String('똥개').josa('이다'), '똥개다')
		self.assertEqual(String('작심삼일').josa('으로'), '작심삼일로')
		self.assertEqual(String('작전변경').josa('로'), '작전변경으로')
		self.assertEqual(String('ㄹ').josa('로'), 'ㄹ로')
		self.assertEqual(String('ㅁ').josa('로'), 'ㅁ으로')
		self.assertEqual(String('311').josa('이라고'), '311이라고')
		self.assertEqual(String('312').josa('이라고'), '312라고')
		self.assertEqual(String('317').josa('라고'), '317이라고')
		self.assertEqual(String('318').josa('으로'), '318로')
		self.assertEqual(String('313').josa('으로'), '313으로')
		self.assertEqual(String('31').josa('으로'), '31로')

	def test_to_hangul(self):
		self.assertEqual(String(11231).to_hangul(), '만천이백삼십일')


if __name__ == '__main__':
	unittest.main()
