import unittest

from . import cutlistat

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class TestGetList(unittest.TestCase):

    def setUp(self):
        self.server = cutlistat.CutListAt()


    def test_getCutListByName(self):
        cutlist=self.server.getCutListByName("2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi")
        self.assertEqual(cutlist.cuts, [ [9061, 20363], [44402, 10857] ])

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

        id=self.server.getListId(xml_list)
        self.assertEqual(id, None, "Malformed XML not detected.")

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

        id=self.server.getListId(xml_list)
        self.assertEqual(id, "9828685", "Empyt rating not correctly parsed.")

if __name__ == '__main__':
    unittest.main()