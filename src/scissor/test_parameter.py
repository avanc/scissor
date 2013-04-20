import unittest

from . import parameter

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class TestParameterParsing(unittest.TestCase):

    def setUp(self):
        pass


    def test_version(self):
        self.assertRaises(SystemExit, parameter.parse, ["--version"])

    def test_help(self):
        self.assertRaises(SystemExit, parameter.parse, ["--help"])

#    def test_wrongLogLevel(self):
#        self.assertRaises(SystemExit, parameter.parse, ["--loglevel=foo"])

#if __name__ == '__main__':
#    unittest.main()