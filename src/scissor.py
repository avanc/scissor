#! /usr/bin/env python

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


from scissor import parameter
from scissor import config
from scissor import otr
from scissor import cut
from scissor.move import regexmove as move

import logging
logger = logging.getLogger()

if __name__ == '__main__':
    options = parameter.parse()
    configdata=config.readConfig(options.configfile)
    
    for inputfile in options.files:
        logger.info("Working on {0}".format(inputfile))
        
        # Decoding
        uncut_avi=otr.decode(inputfile, configdata["otr"])


        #Cutting and renaming        
        cut_avi= cut.cut(uncut_avi, configdata["cut"])
        
        #Moving
        move.move(cut_avi, configdata["move"])
        