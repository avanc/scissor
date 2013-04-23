
import logging
logger = logging.getLogger(__name__)

import re
import shutil


def move(file, config, dryrun=False):
    match=None
    for i in range(len(config["list"])):
        pattern=re.compile(config["list"][i]["regex"])
        if pattern.match(file):
            if (match==None):
                match=i
            else:
                logger.warning("Found more than one regular expression which match {0}: {1} and {2}".format(file, match, i))
                
            logger.info("Moving {0} to folder {1}".format(file, config["list"][i]["destination"]))
            
            if not dryrun:
                shutil.move(file, config["list"][i]["destination"])
    
    return match