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

from . import cutlist

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class TestCutListParsing(unittest.TestCase):

    def setUp(self):
        pass


    def test_parseRawCutList(self):
        import io
        
        raw_cutlist=io.StringIO("""[General]
Application=ColdCut
Version=1.0.8.6
comment1=The following parts of the movie will be kept, the rest will be cut out.
comment2=All values are given in seconds.
ApplyToFile=2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi
OriginalFileSizeBytes=407731250
FramesPerSecond=25
DisplayAspectRatio=16:9
IntendedCutApplicationName=VirtualDub
IntendedCutApplication=VirtualDub.exe
VDUseSmartRendering=1
NoOfCuts=2
[Info]
Author=HardwareFee
RatingByAuthor=4
EPGError=0
ActualContent=
MissingBeginning=0
MissingEnding=0
MissingVideo=0
MissingAudio=0
OtherError=0
OtherErrorDescription=
SuggestedMovieName=2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]
UserComment=Mit ColdCut geschnitten
[Cut0]
Start=362.44
StartFrame=9061
Duration=814.52
DurationFrames=20363
[Cut1]
Start=1776.08
StartFrame=44402
Duration=434.28
DurationFrames=10857""")

        mycutlist=cutlist.parseRaw(raw_cutlist)
        self.assertEqual(mycutlist.cuts, [ [9061, 20363], [44402, 10857] ])

    def test_parseRawCutListWithTime(self):
        import io
        
        raw_cutlist=io.StringIO("""[General]
ApplyToFile=2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi
FramesPerSecond=25
NoOfCuts=2
[Info]
SuggestedMovieName=2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]
[Cut0]
Start=362.44
Duration=814.52
[Cut1]
Start=1776.08
Duration=434.28""")

        mycutlist=cutlist.parseRaw(raw_cutlist)
        logger.debug(mycutlist.cuts)
        self.assertEqual(mycutlist.cuts, [ [9061, 20363], [44402, 10857] ])


    def test_parseRawCutListEmptySuggestedMovieName(self):
        import io
        
        raw_cutlist=io.StringIO("""[General]
ApplyToFile=2_Broke_Girls_13.04.09_21-15_pro7_30_TVOON_DE.mpg.HQ.avi
FramesPerSecond=25
NoOfCuts=2
[Info]
SuggestedMovieName=
[Cut0]
Start=362.44
Duration=814.52
[Cut1]
Start=1776.08
Duration=434.28""")

        mycutlist=cutlist.parseRaw(raw_cutlist)
        logger.debug(mycutlist.cuts)
        self.assertEqual(mycutlist.suggested_filename, None)


    def test_parseRawMalformedCutList(self):
        import io
        
        raw_cutlist=io.StringIO("""[General]
FramesPerSecond=25
NoOfCuts=2
[Info]
Author=HardwareFee
RatingByAuthor=4
EPGError=0
ActualContent=
MissingBeginning=0
MissingEnding=0
MissingVideo=0
MissingAudio=0
OtherError=0
OtherErrorDescription=
SuggestedMovieName=2 Broke Girls - 02x07 - Candy-Andy ist kein Dandy [HQ]
UserComment=Mit ColdCut geschnitten
[Cut0]
Start=362.44
StartFrame=9061
Duration=814.52
DurationFrames=20363""")

        self.assertRaises(KeyError, cutlist.parseRaw, raw_cutlist)
