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


import urllib.request
import xml.etree.ElementTree as ET
import io

from . import cutlist

import logging
logger = logging.getLogger(__name__)


LIST_URL_BY_NAME = "http://www.cutlist.at/getxml.php?name={0}"
LIST_URL_BY_SIZE = "http://www.cutlist.at/getxml.php?ofsb={0}"
FILE_URL_BY_ID = "http://www.cutlist.at/getfile.php?id={0}"
RATE_URL_BY_ID="http://www.cutlist.at/rate.php?rate={id}&rating={rating}"


class CutListAt(object):
    def __init__(self):
        self._list_url_by_name = LIST_URL_BY_NAME
        self._list_url_by_size = LIST_URL_BY_SIZE
        self._file_url_by_id = FILE_URL_BY_ID
        self._rate_url_by_id = RATE_URL_BY_ID
        self._timeout=10
    
    def fetchXmlList(self, name):
        logger.debug("Fetching list for {0}".format(name))
        url = self._list_url_by_name.format(name)
        xml_list = urllib.request.urlopen(url, timeout=self._timeout)
        return xml_list

    def getListId(self, xml_list):
        """Get Id of best cutlist
        
        The lists are weighted according to the rating, ratingcount and downloadcount.
        
        """

        tree = ET.parse(xml_list)
        root = tree.getroot()
        
        # Check if attribute count is the same as contained list descriptions 
        if ( int(root.attrib["count"]) != len(root) ):
            logger.error("Attribute 'count' and number of contained cutlist descriptions differ.")
            raise cutlist.CutListError("Attribute 'count' and number of contained cutlist descriptions differ.")


        bestId= None
        bestWeight=-1;
        
        for child in root:
            cutListId=child.find("id").text
            if cutListId is None:
                raise cutlist.CutListError("No cutlist Id in list.") 
            
            logger.debug("Calculating weight for ID {0}".format(cutListId))
            
            rating=child.find("rating").text
            rating=0.0 if rating==None else float(rating)
            
            ratingcount=child.find("ratingcount").text
            ratingcount=0.0 if ratingcount==None else float(ratingcount)

            downloadcount=child.find("downloadcount").text
            downloadcount=0.0 if downloadcount==None else float(downloadcount)
            
            weight= rating*ratingcount+downloadcount/4
            logger.info("Weight[{4}]={0}*{1}+{2}/4={3}".format(rating, ratingcount, downloadcount, weight, cutListId))
            
            if (weight>bestWeight):
                bestWeight=weight
                bestId=cutListId
                
        return bestId
 
 
    def fetchCutList(self, cutListId):
        logger.debug("Fetching cutlist with ID {0}".format(cutListId))
        url = self._file_url_by_id.format(cutListId)
        logger.debug(url)
        raw_cutlist = urllib.request.urlopen(url, timeout=self._timeout)
        
        # Workaround, as response has no header. Thus, urlopen does not know the encoding and returns binary data.
        # See http://bugs.python.org/issue13518 for additional information.
        raw_cutlist=io.TextIOWrapper(raw_cutlist, encoding='iso-8859-15')
        
        return raw_cutlist
    
    def getCutListByName(self, name):
        xml_list=self.fetchXmlList(name)
        cutListId=self.getListId(xml_list)
        raw_cutlist=self.fetchCutList(cutListId)
        tmpCutlist = cutlist.parseRaw(raw_cutlist)
        tmpCutlist.id=cutListId
        return tmpCutlist
 
    def rateCutList(self, cutlistid, rating):
        cutlist = int(cutlistid)
        rating=int(rating)
        if (rating<0 or rating>5):
            raise ValueError("Rating must be between 0 and 5, not {0}".format(rating))
        url=self._rate_url_by_id.format(id=cutlistid, rating=rating);
        raw_response = urllib.request.urlopen(url, timeout=self._timeout);
        raw_response=io.TextIOWrapper(raw_response, encoding='iso-8859-15');
        output=raw_response.readline()
        logger.debug(output)
        if (output != "Cutlist wurde bewertet. Vielen Dank!"):
            raise RatingFailed(cutlistid, output)

class RatingFailed(Exception):
    """Exception raised for failed rating.

    Attributes:
        id -- cutlist id
    """

    def __init__(self, cutlistid, message):
        self.cutlistid=cutlistid
        self.message=message
        
    def __str__(self):
        return "Failed to rate cutlist {0}: {1}".format(self.cutlistid, self.message)
             
def getCutList(name):
    server=CutListAt();
    return server.getCutListByName(name)

def rateCutList(cutlistid, rating):
    server=CutListAt();
    return server.rateCutList(cutlistid, rating)
