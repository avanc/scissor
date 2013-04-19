import configparser

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CutList():
    def __init__(self):
        self.suggested_filename=None
        self.input_filename=None
        self.output_filename=None
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
        else:
            start=int(float(config[section]["Start"])*cutlist.fps)
            
        if ("DurationFrames" in config[section]):
            duration=int(config[section]["DurationFrames"])
        else:
            duration=int(float(config[section]["Duration"])*cutlist.fps)

        cutlist.cuts.append([start, duration])
    
    return cutlist
    
    