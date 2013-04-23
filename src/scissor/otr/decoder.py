import subprocess
import os
import os.path


import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ToDo: Check if output_path exist
# ToDo: Check if input file exist
# ToDo: Raise exceptions

class OtrDecoder():
    def __init__(self, username, password, working_dir="/tmp/otrdecoder/"):
        self.executable="/usr/bin/otrdecoder"
        self.username=username
        self.password=password
        self.output_path=working_dir
        if (not os.path.exists(self.output_path)):
            os.makedirs(self.output_path)

        
    
    
    def decode(self, filename):
        basename=os.path.basename(filename)
        (decoded_name, extension) = os.path.splitext(basename)
        
        output_filename="{0}/{1}".format(self.output_path, decoded_name)
        
        if (extension!=".otrkey"):
            logger.error("Wrong file extension: {0}".format(basename))
        
        child=subprocess.Popen([self.executable, "-n", "-e", self.username, "-p", self.password,
                                "-i", filename, "-o", self.output_path],
                                bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        
        for line in child.stdout:
            logger.debug(line)
            
            if (line==b'Verifying input ...\n'):
                logger.info("Verifying input file")
                continue
            if (b'Successfully verified input.\n' in line):
                logger.info("Verification successful")
                continue
                
            if (line==b'Check authorization ...\n'):
                logger.info("Checking authorization")
                continue
            if (line==b'Authorized.\n'):
                logger.info("Authorized")
                continue

            if (line==b'Decoding ...\n'):
                logger.info("Decoding input file")
                continue
            if (b'Successfully decoded.\n' in line):
                logger.info("Decoding successful")
                continue
        
            if (line==b'Verifying output ...\n'):
                logger.info("Verifiyng output")
                continue
            if (b'Successfully verified output.\n' in line):
                logger.info("Verifying successful")
                continue

        # Wait to finish avidemux
        success=child.wait()  
      
        if ( (success!=0) or not os.path.exists(output_filename) ):
            logger.warning("Cutting not successful")
            return False
        
        return output_filename
