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

import configparser

import logging
logger = logging.getLogger(__name__)


class CutList(object):
    def __init__(self):
        self.id=None
        self.suggested_filename=None
        self.cuts=[]
        
        
def parseRaw(file):
    cutlist=CutList()
    config = configparser.ConfigParser()
    config.read_file(file)
    
    cutlist.filename=config["General"]["ApplyToFile"]
    cutlist.fps=float(config["General"]["FramesPerSecond"])
    cutcount=int(config["General"]["NoOfCuts"])
    
    cutlist.suggested_filename=config["Info"]["SuggestedMovieName"]
    
    for i in range(cutcount):
        section="Cut{0}".format(i)
        
        if ("StartFrame" in config[section]):
            start=int(config[section]["StartFrame"])
            duration=int(config[section]["DurationFrames"])
        else:
            start=int(float(config[section]["Start"])*cutlist.fps)
            duration=int(float(config[section]["Duration"])*cutlist.fps)

        cutlist.cuts.append([start, duration])
    
    return cutlist

   
class CutListError(Exception):
    """Exception raised for wrong cut lists

    Attributes:
        message -- What happend?
    """

    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return "CutListError: {0}".format(self.message)   