import os
import os.path

from . import cutlistat
from . import avidemux

def cut(input_file, config):
    #Getting cutlist
    (input_path, input_filename)=os.path.split(input_file)
    (input_basename, input_extension) = os.path.splitext(input_filename)
    
    output_path=config["working_dir"]
    if (not os.path.exists(output_path)):
        os.makedirs(output_path)
    
    output_extension=input_extension
    
    cutlist=cutlistat.getCutList(input_filename)

    if ( config["use_suggested_name"]):
        output_basename=cutlist.suggested_filename
    else:
        output_basename=input_basename+"_cut"

    if ( config["append_cutlist_id"]):
        output_basename+="_cutlistat{id}".format(id=cutlist.id)

    output_file="{path}/{base}{ext}".format(path=output_path, base=output_basename, ext=output_extension)
        
    cutter=avidemux.Avidemux()
    cutter.cut(input_file, output_file, cutlist)
    
    return output_file