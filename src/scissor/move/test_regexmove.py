
import unittest

from . import regexmove

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class TestRegExMove(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass


    def testRegularExpression(self):
        config={}
        config["list"]=[]
        item={}
        item["regex"]=".*2_Brocken_Girls.*.avi"
        item["destination"]="/tmp/"
        config["list"].append(item)
        item={}
        item["regex"]=".*2_Broke_Girls.*.avi"
        item["destination"]="/tmp/"
        config["list"].append(item)
        
        
        result=regexmove.move("/data/2_Broke_Girls_blabla.avi", config, dryrun=True)
        self.assertEqual(result, 1, "Didn't selected correct regular expression")


    def testNonUniqueRegularExpression(self):
        config={}
        config["list"]=[]
        item={}
        item["regex"]=".*2_Bro.e_Girls.*.avi"
        item["destination"]="/tmp1/"
        config["list"].append(item)
        item={}
        item["regex"]=".*2_Broke_Girls.*.avi"
        item["destination"]="/tmp/"
        config["list"].append(item)
        
        
        result=regexmove.move("/data/2_Broke_Girls_blabla.avi", config, dryrun=True)
        self.assertEqual(result, 0, "Didn't selected correct regular expression")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()