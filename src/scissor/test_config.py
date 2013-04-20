
import unittest

from . import config

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class TestConfig(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass


    def testRawData(self):
        jsondata="""{ "2 Broke Girls" : {"regex" : "*2_Broke_Girls*",
                                         "destination": "/data/videos/Serien/2_Broke_Girls"} }"""
        realdata={}
        realdata["2 Broke Girls"]={}
        realdata["2 Broke Girls"]["regex"]="*2_Broke_Girls*"
        realdata["2 Broke Girls"]["destination"]="/data/videos/Serien/2_Broke_Girls"
        data=config.parseConfig(jsondata)
        self.assertEqual(realdata, data)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()