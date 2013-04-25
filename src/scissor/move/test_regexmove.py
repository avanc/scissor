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
