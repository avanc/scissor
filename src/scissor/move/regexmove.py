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


import re
import shutil

import logging
logger = logging.getLogger(__name__)


def move(file, config, dryrun=False):
    logger.debug("Searching match for {0}".format(file))
    regex_number=None
    for i in range(len(config["list"])):
        logger.debug("Testing {0}".format(config["list"][i]["regex"]))
        pattern=re.compile(config["list"][i]["regex"])
        if pattern.match(file):
            if (regex_number==None):
                regex_number=i
            else:
                logger.warning("Found more than one regular expression which match {0}: {1} and {2}".format(file, regex_number, i))
                
            logger.info("Moving {0} to folder {1}".format(file, config["list"][i]["destination"]))
            
            if not dryrun:
                shutil.move(file, config["list"][i]["destination"])
    
    return regex_number