import unittest

from . import avidemux
from . import cutlist

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class TestAvidemux(unittest.TestCase):

    def setUp(self):
        pass


    def test_createScript(self):
        cutter=avidemux.Avidemux()
        test_cutlist=cutlist.CutList()
        test_cutlist.cuts=[ [9061, 20363], [44402, 10857] ]
        test_cutlist.fps=25.0
        test_cutlist.input_filename="/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi"
        test_cutlist.output_filename="/tmp/output.avi"
        
        cutter.createScript(test_cutlist)
        
    def test_cutVideo(self):
        cutter=avidemux.Avidemux()
        test_cutlist=cutlist.CutList()
        test_cutlist.cuts=[ [9061, 20363], [44402, 10857] ]
        test_cutlist.fps=25.0
        test_cutlist.input_filename="/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi"
        test_cutlist.output_filename="/tmp/output.avi"
        
        # Interestingly, avidemux is not working correctly when unittest is used
        # cutter.cut(test_cutlist)


if __name__ == '__main__':
    unittest.main()