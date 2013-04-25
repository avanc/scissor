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

