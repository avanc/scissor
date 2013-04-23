#! /usr/bin/env python

import logging
logger = logging.getLogger()


from scissor import parameter
from scissor import config
from scissor import otr
from scissor import cut
from scissor.move import regexmove as move

if __name__ == '__main__':
    options = parameter.parse()
    configdata=config.readConfig(options.configfile)
    
    for inputfile in options.files:
        logger.info("Working on {0}".format(inputfile))
        
        # Decoding
        otrdecoder=otr.OtrDecoder(configdata["otr"])
        uncut_avi=otrdecoder.decode(inputfile)


        #Cutting and renaming        
        cut_avi= cut.cut(uncut_avi, configdata["cut"])
        
        #Moving
        move.move(cut_avi, configdata["move"])
        
        
        
        # Moving
        
        
        