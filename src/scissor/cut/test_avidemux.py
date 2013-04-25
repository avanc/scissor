# Copyright (C) 2013 Sven Klomp (mail@klomp.eu)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

import unittest

from . import avidemux
from . import cutlist

from .. import error

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class TestAvidemux(unittest.TestCase):

    def setUp(self):
        self.cutter=avidemux.Avidemux()
        self.cutlist=cutlist.CutList()
        self.cutlist.cuts=[ [9061, 20363], [44402, 10857] ]
        self.cutlist.fps=25.0

    def test_createScript(self):
        input_filename="/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi"
        output_filename="/tmp/output.avi"
        
        self.cutter.createScript(input_filename, output_filename, self.cutlist)
        
        
    def test_existing_output_file(self):
        self.assertRaises(FileExistsError, self.cutter.cut, "/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi", "/tmp/output.avi", self.cutlist)

    def test_non_existing_file(self):
        self.assertRaises(FileNotFoundError, self.cutter.cut, "/tmp/foo.avi", "/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ_cut.avi", self.cutlist)

    def test_wrong_file_type(self):
        self.assertRaises(error.WrongFileTypeError, self.cutter.cut, "/tmp/foo.mpg", "/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ_cut.avi", self.cutlist)

        
        
    def test_cutVideo(self):
        cutter=avidemux.Avidemux()
        test_cutlist=cutlist.CutList()
        test_cutlist.cuts=[ [9061, 20363], [44402, 10857] ]
        test_cutlist.fps=25.0
        input_filename="/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi"
        output_filename="/tmp/output.avi"
        
        result=cutter.cut(input_filename, output_filename, test_cutlist)
        self.assertTrue(result, "Not detected failed cut.")

