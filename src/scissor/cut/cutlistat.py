import urllib.request
import xml.etree.ElementTree as ET
import io

from . import cutlist

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

getListUrlByName = "http://www.cutlist.at/getxml.php?name={0}"
getListUrlBySize = "http://www.cutlist.at/getxml.php?ofsb={0}"
getFileUrl = "http://www.cutlist.at/getfile.php?id={0}"


class CutListAt:
    def __init__(self):
        self.base_url="http://www.cutlist.at/getxml.php"
    
    def fetchXmlList(self, name):
        logger.debug("Fetching list for {0}".format(name))
        url = getListUrlByName.format(name)
        xml_list = urllib.request.urlopen(url)
        return xml_list

    def getListId(self, xml_list):
        """Get Id of best cutlist
        
        The lists are weighted according to the rating, ratingcount and downloadcount.
        
        """

        tree = ET.parse(xml_list)
        root = tree.getroot()
        
        # Check if attribute count is the same as contained list descriptions 
        if ( int(root.attrib["count"]) != len(root) ):
            logger.warning("Attribute 'count' and number of contained cutlist descriptions differ.")
            return None

        bestId= None
        bestWeight=-1;
        
        for child in root:
            cutListId=child.find("id").text
            logger.debug("Calculating weight for ID {0}".format(cutListId))
            
            rating=child.find("rating").text
            rating=0.0 if rating==None else float(rating)
            
            ratingcount=child.find("ratingcount").text
            ratingcount=0.0 if ratingcount==None else float(ratingcount)

            downloadcount=child.find("downloadcount").text
            downloadcount=0.0 if downloadcount==None else float(downloadcount)
            
            weight= rating*ratingcount+downloadcount/4
            logger.debug("Weight={0}*{1}+{2}/4={3}".format(rating, ratingcount, downloadcount, weight))
            
            if (weight>bestWeight):
                bestWeight=weight
                bestId=cutListId
                
        return bestId
 
 
    def fetchCutList(self, cutListId):
        logger.debug("Fetching cutlist with ID {0}".format(cutListId))
        url = getFileUrl.format(cutListId)
        logger.debug(url)
        raw_cutlist = urllib.request.urlopen(url)
        
        # Workaround, as response has no header. Thus, urlopen does not know the encoding and returns binary data.
        # See http://bugs.python.org/issue13518 for additional information.
        raw_cutlist=io.TextIOWrapper(raw_cutlist, encoding='utf-8')
        
        return raw_cutlist
    
    def getCutListByName(self, name):
        xml_list=self.fetchXmlList(name)
        cutListId=self.getListId(xml_list)
        raw_cutlist=self.fetchCutList(cutListId)
        return cutlist.parseRaw(raw_cutlist)
           
        