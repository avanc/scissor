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

from . import decoder
from .. import error

# Credentials for otr authentication moved to an external file
from . import otr_credentials


import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class TestOtrDecoder(unittest.TestCase):

    def setUp(self):

        self.decoder=decoder.OtrDecoder(otr_credentials.username, otr_credentials.password)


    def test_decodeFile(self):
        result=self.decoder.decode("/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.otrkey")
        self.assertTrue(result, "Decoding failed.")

    def test_existing_output_file(self):
        self.assertRaises(FileExistsError, self.decoder.decode, "/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.otrkey")

    def test_non_existing_file(self):
        self.assertRaises(FileNotFoundError, self.decoder.decode, "/tmp/foobar.otrkey")

    def test_wrong_file_type(self):
        self.assertRaises(error.WrongFileTypeError, self.decoder.decode, "/tmp/foobar.avi")

    def test_wrongUserCredentials(self):
        self.decoder=decoder.OtrDecoder("foo", "bar")
        result=self.decoder.decode("/home/klomp/tmp/cutlist/2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi.otrkey")
        self.assertFalse(result, "Failed decoding not detected.")

        