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

"""This module wraps the external otrdecoder."""

import subprocess
import os.path

from .. import error 

import logging
logger = logging.getLogger(__name__)


# ToDo: Check otrdecoder output on fail, to provide better error messages (e.g. wrong email/password

class OtrDecoder(object):
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
            raise error.WrongFileTypeError(filename, ".otrkey")

        if not os.path.isfile(filename):
            logger.error("File not found: {0}".format(filename))
            raise FileNotFoundError(filename)
        
        if (os.path.exists(output_filename)):
            logger.error("Output file already exists: {0}".format(output_filename))
            raise FileExistsError(output_filename)
             
        
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
                logger.info("Verifying output")
                continue
            if (b'Successfully verified output.\n' in line):
                logger.info("Verifying successful")
                continue

        # Wait to finish avidemux
        success=child.wait()  
      
        if ( (success!=0) or not os.path.exists(output_filename) ):
            logger.error("Decoding was not successful.")
            raise ChildProcessError()
        
        return output_filename