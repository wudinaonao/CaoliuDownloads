import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])

from Tools.Log import Log as logger
from Tools.GeneralTool import GeneralTool
from DataBase.DBUtil import DBUtil
from Tools.PyAria2 import PyAria2
from Config.Config import ARIA2_HOST
from Config.Config import ARIA2_PORT
from Config.Config import ARIA2_TOKEN
from Config.Config import ARIA2_LINK_TYPE
from Config.Config import ARIA2_SAVE_PATH

class Video(GeneralTool):
    
    def __init__(self):
        
        self._pyaria2 = PyAria2(host=ARIA2_HOST,
                                port=ARIA2_PORT,
                                token=ARIA2_TOKEN,
                                link_type=ARIA2_LINK_TYPE)
        self._database = DBUtil()
        self._completed = 0
        self._totalDownload = 0
        
    def torrentResultDictGenerator(self):
        torrentResultDictList = self._database.query("torrent", {"downloaded": 0})
        self._totalDownload = len(torrentResultDictList)
        logger.info("not downloaded torrent count {0}".format(len(torrentResultDictList)))
        for torentResultDict in torrentResultDictList:
            yield torentResultDict
    
    def getSavePath(self, torrentResultDict):
        categoryName = self.getCategoryFromDatailsPageUrl(torrentResultDict["detailsPageUrl"])
        if ARIA2_SAVE_PATH:
            torrentPath = self.checkAria2SavePath(os.path.join(ARIA2_SAVE_PATH,
                                                               "video",
                                                               categoryName,
                                                               self.year(),
                                                               self.month(),
                                                               self.day())
                                                  )

            return torrentPath
        else:
            return None
        
    def addToAria2(self, torentResultDict):
        magnet = torentResultDict["magnet"]
        savePath = self.getSavePath(torentResultDict)
        torrenName = torentResultDict["title"]
        logger.info("add to aria2, torrent file: {0}".format(torrenName))
        self._pyaria2.addUrls(magnet, savePath)
        self._completed += 1
        
    def downloadScheduler(self):
        for torentResultDict in self.torrentResultDictGenerator():
            self.addToAria2(torentResultDict)
            updateDownloaded = {
                "key_values":{
                    "downloaded": "1"
                },
                "postions":{
                    "md5": torentResultDict["md5"]
                }
            }
            self._database.update("torrent", updateDownloaded)
    
if __name__ == '__main__':
    
    video = Video()
    video.downloadScheduler()
    
    
    
    