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


import subprocess
import os

from .. import error

import logging
logger = logging.getLogger(__name__)


# Information on avidemux scripting at
# http://www.avidemux.org/admWiki/doku.php?id=tutorial:scripting_tutorial
SCRIPT_TEMPLATE="""//AD <- Needed to identify//
var app = new Avidemux();

app.load("{input_filename}");
// app.rebuildIndex();

app.clearSegments();
{segments}

app.video.setPostProc(3,3,0);
app.video.fps1000={fpks};
app.video.codec("Copy","CQ=4","0 ");

app.audio.reset();
app.audio.codec("copy",128,0,"");
app.audio.normalizeMode=0;
app.audio.normalizeValue=0;
app.audio.delay=0;
app.audio.mixer="NONE";
app.audio.scanVBR="";
//app.setContainer("AVI");
setSuccess(app.save("{output_filename}"));

//End of script
"""

SEGMENT_TEMPLATE="app.addSegment(0,{start_frame},{durationframes});\n"


class Avidemux():
    def __init__(self, working_dir="/tmp/"):
        self.executable="/usr/bin/avidemux2_cli"
        self.verbose=True
        self.script_path=working_dir
        if (not os.path.exists(self.script_path)):
            os.makedirs(self.script_path)
            
    def createScript(self, input_file, output_file, cutlist):
        segments=""
        for cut in cutlist.cuts:
            segments+=SEGMENT_TEMPLATE.format(start_frame=cut[0], durationframes=cut[1])
        
        script=SCRIPT_TEMPLATE.format(input_filename=input_file, segments=segments, fpks=int(cutlist.fps*1000), output_filename=output_file)
        
        return script


    def cut(self, input_file, output_file, cutlist):
        (base, extension) = os.path.splitext(input_file)
        if (extension!=".avi"):
            logger.error("Wrong file extension: {0}".format(input_file))
            raise error.WrongFileTypeError(input_file, ".avi")

        if not os.path.isfile(input_file):
            logger.error("File not found: {0}".format(input_file))
            raise FileNotFoundError(input_file)
        
        if (os.path.exists(output_file)):
            logger.error("Output file already exists: {0}".format(output_file))
            raise FileExistsError(output_file)

        script=self.createScript(input_file, output_file, cutlist)

        script_file="{path}/cutscript_{id}.js".format(path=self.script_path, id=cutlist.id)
        f=open(script_file,"w")
        f.write(script)
        f.close()
     
        result=self.run(script_file)

        if (result):
            return os.path.exists(output_file)
        else:
            raise ChildProcessError()
        
    def run(self, script_file):
        logger.info("Starting avidemux")
        
        
        child=subprocess.Popen([self.executable, "--nogui", "--force-smart", "--run", script_file, "--quit"],
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
            raise ChildProcessError()
        
        return True
        