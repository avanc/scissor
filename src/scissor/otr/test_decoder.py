import unittest

from . import decoder

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class TestOtrDecoder(unittest.TestCase):

    def setUp(self):
        self.decoder=decoder.OtrDecoder("email", "password")


    def test_decodeFile(self):
        result=self.decoder.decode("/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.otrkey")
        self.assertTrue(result, "Decoding failed.")

    def test_existingFile(self):
        result=self.decoder.decode("/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.otrkey")
        self.assertFalse(result, "Failed decoding not detected.")

    def test_wrongFilename(self):
        result=self.decoder.decode("/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.xxxxxxxx")
        self.assertFalse(result, "Failed decoding not detected.")

    def test_wrongUserCredentials(self):
        self.decoder=decoder.OtrDecoder("foo", "bar")
        result=self.decoder.decode("/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.otrkey")
        self.assertFalse(result, "Failed decoding not detected.")


if __name__ == '__main__':
    unittest.main()