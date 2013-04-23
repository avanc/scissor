
import subprocess
import os

import logging
logger = logging.getLogger(__name__)


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
    
    def createScript(self, input_file, output_file, cutlist):
        segments=""
        for cut in cutlist.cuts:
            segments+=segment_template.format(start_frame=cut[0], durationframes=cut[1])
        
        script=script_template.format(input_filename=input_file, segments=segments, output_filename=output_file)
        
        #logger.debug(script)
        
        return script


    def cut(self, input_file, output_file, cutlist):
        script=self.createScript(input_file, output_file, cutlist)

        script_file=self.tmpFolder+"/cutscript_{id}.js".format(id=cutlist.id)
        f=open(script_file,"w")
        f.write(script)
        f.close()
     
        result=self.run(script_file)

        if (result):
            return os.path.exists(output_file)
        else:
            return False
        
    def run(self, script_file):
        logger.debug("Starting avidemux")
        
        
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
        