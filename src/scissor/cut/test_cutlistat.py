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
import urllib.error
import xml.etree.ElementTree

from . import cutlistat
from . import cutlist

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class TestGetList(unittest.TestCase):

    def setUp(self):
        self.server = cutlistat.CutListAt()


    def test_getCutListByName(self):
        cutlist=self.server.getCutListByName("2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi")
        self.assertEqual(cutlist.cuts, [ [9061, 20363], [44402, 10857] ])

    def test_server_not_available(self):
        self.server._list_url_by_name="http://192.168.111.1/{0}"
        self.server._timeout=1
        self.assertRaises(urllib.error.URLError, self.server.fetchXmlList, "2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi")

    def test_wrong_url(self):
        self.server._list_url_by_name="http://www.cutlist.at/getml.php?name={0}"
        self.server._timeout=1
        self.assertRaises(urllib.error.URLError, self.server.fetchXmlList, "2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi")


    def test_parseXml(self):
        import io
        
        xml_list=io.StringIO("""<?xml version="1.0" encoding="iso-8859-1" ?>
            <files count="2">
                <cutlist row_index="0">
                    <id>9828685</id>
                    <name>2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.cutlist</name>
                    <rating>4.50</rating>
                    <ratingcount>4</ratingcount>
                    <filename>2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]</filename>
                    <filename_original>2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]</filename_original>
                    <withframes>1</withframes>
                    <withtime>1</withtime>
                    <duration>1248.8</duration>
                    <errors>000000</errors>
                    <othererrordescription></othererrordescription>
                    <downloadcount>47</downloadcount>
                </cutlist>
                <cutlist row_index="1">
                    <id>9828700</id>
                    <name>2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.cutlist</name>
                    <rating></rating>
                    <ratingcount>0</ratingcount>
                    <filename>2 Broke Girls S02E07 Candy-Andy ist kein Dandy</filename>
                    <filename_original>2 Broke Girls S02E07 Candy-Andy ist kein Dandy</filename_original>
                    <withframes>0</withframes>
                    <withtime>1</withtime>
                    <duration>850.72</duration>
                    <errors>000000</errors>
                    <othererrordescription></othererrordescription>
                    <downloadcount>2</downloadcount>
                </cutlist>
            </files>""")

        self.server.getListId(xml_list)

    def test_parseMalformedXml(self):
        import io
        
        xml_list=io.StringIO("""<?xml version="1.0" encoding="iso-8859-1" ?>
            <files count="2">
                <cutlist row_index="0">
                    <id>9828685</id>
                    <name>2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.cutlist</name>
                    <rating>4.50</rating>
                    <ratingcount>4</ratingcount>
                    <filename>2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]</filename>
                    <filename_original>2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]</filename_original>
                    <withframes>1</withframes>
                    <withtime>1</withtime>
                    <duration>1248.8</duration>
                    <errors>000000</errors>
                    <othererrordescription></othererrordescription>
                    <downloadcount>47</downloadcount>
                </cutlist>
            </files>""")

        self.assertRaises(cutlist.CutListError, self.server.getListId, xml_list)

    def test_parseMalformedXml2(self):
        import io
        
        xml_list=io.StringIO("""<?xml version="1.0" encoding="iso-8859-1" ?>
            <files count="2">
                <cutlist row_index="0">
                    <name>2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.cutlist</name>
                    <rating>4.50</rating>
                    <ratingcount>4</ratingcount>
                    <filename>2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]</filename>
                    <filename_original>2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]</filename_original>
                    <withframes>1</withframes>
                    <withtime>1</withtime>
                    <duration>1248.8</duration>
                    <errors>000000</errors>
                    <othererrordescription></othererrordescription>
                    <downloadcount>47</downloadcount>
                </cutlist>
            </files>""")

        self.assertRaises(cutlist.CutListError, self.server.getListId, xml_list)

    def test_parseMalformedXml3(self):
        import io
        
        xml_list=io.StringIO("""Hello World""")

        self.assertRaises(xml.etree.ElementTree.ParseError, self.server.getListId, xml_list)

    
    def test_parseXmlWithEmptyRating(self):
        import io
        
        xml_list=io.StringIO("""<?xml version="1.0" encoding="iso-8859-1" ?>
            <files count="1">
                <cutlist row_index="0">
                    <id>9828685</id>
                    <name>2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.cutlist</name>
                    <rating></rating>
                    <ratingcount>4</ratingcount>
                    <filename>2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]</filename>
                    <filename_original>2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]</filename_original>
                    <withframes>1</withframes>
                    <withtime>1</withtime>
                    <duration>1248.8</duration>
                    <errors>000000</errors>
                    <othererrordescription></othererrordescription>
                    <downloadcount>47</downloadcount>
                </cutlist>
            </files>""")

        cutlist_id=self.server.getListId(xml_list)
        self.assertEqual(cutlist_id, "9828685", "Empty rating not correctly parsed.")

