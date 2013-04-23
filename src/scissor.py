#! /usr/bin/env python

import logging
logger = logging.getLogger()


import os.path

from scissor import parameter
from scissor import config
from scissor.otr import decoder

from scissor.cut import cutlistat
from scissor.cut import avidemux

if __name__ == '__main__':
    options = parameter.parse()
    configdata=config.readConfig(options.configfile)
    
    for inputfile in options.files:
        logger.info("Working on {0}".format(inputfile))
        
        # Decoding
        otrdecoder=decoder.OtrDecoder(configdata["otr"]["email"], configdata["otr"]["password"])
        otrdecoder.output_path=configdata["working_dir"]+ "/decoded/"
        
        new_file=otrdecoder.decode(inputfile)
        
        #Cutting and renaming        
        mycutlistat=cutlistat.CutListAt()
        cutlist=mycutlistat.getCutListByName(os.path.basename(new_file))
        cutlist.input_filename=new_file
        
        if (configdata["use_suggested_name"]):
            cutlist.output_filename="{0}/{1}{3}".format(os.path.dirname(new_file), cutlist.suggested_filename, ".avi")
        else:
            (base, extension) = os.path.splitext(new_file)
            cutlist.output_filename="{0}_cut{1}".format(base, extension)
            
        if (configdata["append_cutlist_id"]):
            (base, extension) = os.path.splitext(cutlist.output_filename)
            cutlist.output_filename="{0}_cutlistat{1}{2}".format(base, cutlist.id, extension)
        
        cutter=avidemux.Avidemux()
        cutter.cut(cutlist)
        
        
        
        
        
        # Moving
        
        
        