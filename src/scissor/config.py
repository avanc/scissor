
import logging
logger = logging.getLogger(__name__)


import json
import os.path

def parseConfig(jsonstring):
    data=json.loads(jsonstring)
    return data

def readConfig(filename):
    fp=open(os.path.expanduser(filename))
    data=json.load(fp)
    return data