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
        input_filename="/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi"
        output_filename="/tmp/output.avi"
        
        cutter.createScript(input_filename, output_filename, test_cutlist)
        
    def test_cutVideo(self):
        cutter=avidemux.Avidemux()
        test_cutlist=cutlist.CutList()
        test_cutlist.cuts=[ [9061, 20363], [44402, 10857] ]
        test_cutlist.fps=25.0
        input_filename="/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi"
        output_filename="/tmp/output.avi"
        
        result=cutter.cut(input_filename, output_filename, test_cutlist)
        self.assertTrue(result, "Not detected failed cut.")

    def test_cutVideoFailing(self):
        cutter=avidemux.Avidemux()
        test_cutlist=cutlist.CutList()
        test_cutlist.cuts=[ [9061, 20363], [44402, 10857] ]
        test_cutlist.fps=25.0
        input_filename="/home/klomp/tmp/cutlist/xxxxxxxxx"
        output_filename="/tmp/output2.avi"
        
        result=cutter.cut(input_filename, output_filename, test_cutlist)
        self.assertFalse(result, "Not detected failed cut.")



if __name__ == '__main__':
    unittest.main()