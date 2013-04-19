
import subprocess
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Information on avidemux scripting at
# http://www.avidemux.org/admWiki/doku.php?id=tutorial:scripting_tutorial
script_template="""//AD <- Needed to identify//
var app = new Avidemux();

app.load("{input_filename}");
app.rebuildIndex();

app.clearSegments();
{segments}

app.video.setPostProc(3,3,0);
app.video.fps1000=25000;
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
segment_template="app.addSegment(0,{start_frame},{durationframes});\n"


class Avidemux():
    def __init__(self):
        self.executable="/usr/bin/avidemux2_cli"
        self.verbose=True
        self.tmpFolder="/tmp"
    
    def createScript(self, cutlist):
        segments=""
        for cut in cutlist.cuts:
            segments+=segment_template.format(start_frame=cut[0], durationframes=cut[1])
        
        script=script_template.format(input_filename=cutlist.input_filename, segments=segments, output_filename=cutlist.output_filename)
        
        #logger.debug(script)
        
        return script


    def cut(self, cutlist):
        script=self.createScript(cutlist)
        result=self.run(script)
        if (result):
            return os.path.exists(cutlist.output_filename)
        else:
            return False
        
    def run(self, script):
        logger.debug("Starting avidemux")
        
        script_file=self.tmpFolder+"/project.js"
        f=open(script_file,"w")
        f.write(script)
        f.close()
        
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
            return False
        
        return True
        