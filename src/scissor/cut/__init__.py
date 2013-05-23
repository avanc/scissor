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

import os
import os.path

import logging
logger = logging.getLogger(__name__)

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

    output_basename=input_basename+"_cut"
    if ( config["use_suggested_name"]):
        if (cutlist.suggested_filename==None):
            logger.warning("Suggested filename was empty.")
        else:
            output_basename=cutlist.suggested_filename


    if ( config["append_cutlist_id"]):
        output_basename+="_cutlistat{id}".format(id=cutlist.id)

    output_file="{path}/{base}{ext}".format(path=output_path, base=output_basename, ext=output_extension)
        
    cutter=avidemux.Avidemux(config["working_dir"])
    cutter.cut(input_file, output_file, cutlist)
    
    return output_file