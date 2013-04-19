import subprocess

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OtrDecoder():
    def __init__(self, username, password):
        self.executable="/usr/bin/otrdecoder"
        self.username=username
        self.password=password
        self.output_path="/tmp"
        self.verbose=True
    
    
    def decode(self, filename):
        child=subprocess.Popen([self.executable, "-e", self.username, "-p", self.password,
                                "-i", filename, "-o", self.output_path],
                                bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        if (self.verbose):
            output=True
            while (output):
                output=child.stdout.readline()
                logger.debug(output)
        else:
            pass
        
        # Wait to finish avidemux
        success=child.wait()  
      
        if (success!=0):
            logger.warning("Cutting not successful")
            return False
        
        return True
