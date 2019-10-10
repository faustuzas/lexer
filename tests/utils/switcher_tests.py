from unittest import TestCase

from utils import Switcher, letters


class SwitcherTests(TestCase):
    switch = Switcher.from_dict({
        't': lambda: 'char',
        4: lambda: 'number',
        range(10): lambda: 'number range',
        letters: lambda: 'letters range'
    }, lambda: 'default')

    def test_matches_number(self):
        self.assertEquals('number', self.switch.exec(4))

    def test_matches_char(self):
        self.assertEquals('char', self.switch.exec('t'))

    def test_matches_number_range(self):
        self.assertEquals('number range', self.switch.exec(8))

    def test_matches_letter_range(self):
        self.assertEquals('letters range', self.switch.exec('z'))

    def test_returns_default(self):
        self.assertEquals('default', self.switch.exec('@'))
