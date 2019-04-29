import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])

import platform
import bencodepy
import hashlib
import base64
from datetime import datetime
from Tools.Log import Log as logger
from Tools.AsyncRequests import AsyncRequests
from Config.Config import DOWNLOAD_CONCURRENT_COUNT
from bs4 import BeautifulSoup as bs
import traceback
import re
import os
from Constant import Category
from DataBase.DBUtil import DBUtil
from Config.Config import TIME_OUT
from Config.Config import ARIA2_SAVE_PATH


class GeneralTool():
    
    _database = DBUtil()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
    }

    excludeUrlList = [
        'htm_data/16/1106/524942.html',
        'htm_data/16/1808/344501.html',
        'htm_data/16/1707/2519480.html',
        'htm_data/2/1111/30611.html',
        'htm_data/16/1706/2424348.html',
        'htm_data/16/1110/622028.html',
        'htm_data/16/0805/136474.html',
        'htm_data/16/1109/594741.html',
        'read.php?tid=5877',
        'read.php?tid',
        'htm_data/4/1106/524586.html',
        'htm_data/5/1707/2519502.html',
        'htm_data/5/1106/517566.html',
        'htm_data/4/1206/756654.html',
        '344501.html'
    ]

    domains = "https://www.t66y.com/"
    xpath = "//td[@class='tal']/h3/a/@href"

    @classmethod
    def urlInExclued(cls, url):
        for excluedUrl in cls.excludeUrlList:
            if excluedUrl in url:
                return True
        return False
    
    @classmethod
    def checkSystemType(cls):
        if "windows" in str(platform.platform()).lower():
            return "windows"
        elif "linux" in str(platform.platform()).lower():
            return "linux"
        else:
            return "unknown"
        
    @classmethod
    def checkDirExist(cls, originPath):
        '''
        check dir exist
        :param originPath:
        :return: return torrent save full path
        '''
        dirPath = os.path.split(originPath)[0]
        torrentName = os.path.split(originPath)[1]
        if cls.checkSystemType() == "windows":
            # if config save path is absolute
            if ":" in dirPath:
                if not os.path.isdir(dirPath):
                    os.makedirs(dirPath)
                return originPath
            else:
                currentDir = os.path.split(os.getcwd())[0]
                saveDirPath = os.path.join(currentDir, dirPath)
                if not os.path.isdir(saveDirPath):
                    os.makedirs(saveDirPath)
                return os.path.join(saveDirPath, torrentName)
        elif cls.checkSystemType() == "linux":
            # check dir exist
            if not os.path.isdir(dirPath):
                os.makedirs(dirPath)
            return originPath
        else:
            # check dir exist
            if not os.path.isdir(dirPath):
                os.makedirs(dirPath)
            return originPath
    
    @classmethod
    def checkAria2SavePath(cls, savePath):
        if not savePath:
            return savePath
        if "/" in ARIA2_SAVE_PATH:
            return savePath.replace("\\", "/")
        else:
            return savePath.replace("/", "\\")
    
    @classmethod
    def computeMD5(cls, title, url, dataStr):
        title = str(title)
        url = str(url)
        dataStr = str(dataStr)
        string = title.lower() + url.lower() + dataStr.lower()
        md5Str = hashlib.md5()
        md5Str.update(string.encode(encoding='utf-8'))
        return md5Str.hexdigest().upper()

    @classmethod
    def computeMD5ByFile(cls, torrentFileByte):
        md5Str = hashlib.md5()
        md5Str.update(torrentFileByte)
        return md5Str.hexdigest().upper()
        
    @classmethod
    def torrentToMagnet(cls, torrentByte):
        try:
            metadata = bencodepy.decode(torrentByte)
            subj = metadata[b'info']
            hashcontents = bencodepy.encode(subj)
            digest = hashlib.sha1(hashcontents).digest()
            b32hash = base64.b32encode(digest).decode()
            return 'magnet:?' \
                   + 'xt=urn:btih:' + b32hash
        except:
            return ""
        
    @classmethod
    def formatDate(cls):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    @classmethod
    def year(cls):
        return str(datetime.now().strftime('%Y'))
    
    @classmethod
    def month(cls):
        return str(datetime.now().strftime('%m'))
    
    @classmethod
    def day(cls):
        return str(datetime.now().strftime('%d'))
    
    @classmethod
    def isDownloadPageUrl(cls, url):
        '''
        is download page url
        :param url:
        :return:
        '''
        if "rmdown.com" in url:
            return True
        else:
            return False

    @classmethod
    def isImageDownloadPageUrl(cls, url):
        return True
    
    @classmethod
    def torrentDownloadUrl(cls, responseText):
        '''
        get torrent download url from download page
        :param responseText: response text not response
        :return:
        '''
        soup = bs(responseText, "lxml")
        inputTagList = soup.find_all("input")
        reff = ""
        ref = ""
        torrentDownloadUrl = ""
        for inputTag in inputTagList:
            if inputTag["name"] == "reff":
                reff = str(inputTag["value"])
            elif inputTag["name"] == "ref":
                ref = str(inputTag["value"])
        if reff and ref:
            torrentDownloadUrl = "http://www.rmdown.com/download.php?reff={0}&ref={1}".format(reff, ref)
        if torrentDownloadUrl:
            return torrentDownloadUrl
        else:
            return None

    @classmethod
    def urlToResponse(cls, urlList, cookies=None, timeOut=TIME_OUT):
        
        requestsList = []
        for url in urlList:
            if cookies:
                request = AsyncRequests.get(url=url, headers=cls.headers, cookies=cookies, timeout=timeOut)
            else:
                request = AsyncRequests.get(url=url, headers=cls.headers, timeout=timeOut)
            requestsList.append(request)
        resultList = AsyncRequests.map(requestsList, size=DOWNLOAD_CONCURRENT_COUNT)
        return resultList

    @classmethod
    def filterTorrentName(cls, torrentName):
        try:
            torrentName = re.sub(r'[？\\*|“<>:/]', '', torrentName)
            torrentName = re.sub(r'[\/\\\:\*\?\"\<\>\|]', '', torrentName)
            return torrentName
        except BaseException:
            logger.error(traceback.format_exc())
            return torrentName

    @classmethod
    def removeDepulicates(cls, inputList):
        newList = []
        for element in inputList:
            if not element in newList:
                newList.append(element)
        return newList

    @classmethod
    def getCategoryFromDatailsPageUrl(cls, detailsPageUrl):
        try:
            return Category.categoryNumberToNameDict[str(detailsPageUrl.split("/")[4])]
        except BaseException:
            logger.error(traceback.format_exc())
            return "unknown"

    @classmethod
    def clearTitle(cls, title):
        try:
            title = title.split(" - ")[0]
            title = title.replace("\xa0", "")
            return title
        except BaseException:
            logger.error(traceback.format_exc())
            return title
    
    @classmethod
    def computeProgressBar(cls, currentValue, maxValue):
        return str(round((float(currentValue) / float(maxValue)), 4) * 100)[:5] + "%"
    
    @classmethod
    def existInDatabase(cls, tableName, position):
        result = cls._database.queryIsExist(tableName, position)
        try:
            if result:
                return True
            else:
                return False
        except BaseException:
            logger.error(traceback.format_exc())
            return False
    
    @classmethod
    def testCode(cls):
        result = cls._database.query("video", {"md5":"7034677AC329006F5B2F54D69180F1E1"})
        pass
if __name__ == '__main__':
    # torrentPath = GeneralTool.checkDirExist(os.path.join("CAOLIU", "torrent", "1.torrent"))
    # pass
    # print(torrentPath)
    GeneralTool.testCode()
    # print(GeneralTool.checkSystemType())