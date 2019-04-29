import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])

from Config.Config import TRACKING_PAGE_COUNT
from Config.Config import DOWNLOAD_CONCURRENT_COUNT
from Config.Config import BT_DOWNLOAD_CATEGORY
from Config.Config import COOKIES
from Config.Config import SAVE_PATH
from Spider.ResultClass.TorrentResultClass import TorrentResultClass
from Tools.AsyncRequests import AsyncRequests
from bs4 import BeautifulSoup as bs
from Tools.Log import Log as logger
import traceback
from Constant import Category
from Tools.GeneralTool import GeneralTool
from DataBase.DBUtil import DBUtil
import requests

class Torrent(GeneralTool):
    
    def __init__(self, queue):
        
        self._database = DBUtil()
        self._taskQueue = queue
        self._queueProducerStatus = True
        self.completed = 0
        self.totalDownload = 0
    
    def generatorListPage(self):
        '''
        generator list page url
        :return: response list
        '''
        
        # check track page count is vailed
        # track page count is 100 if track too many
        trackingPageCount = TRACKING_PAGE_COUNT
        if isinstance(trackingPageCount, int):
            if trackingPageCount > 100:
                trackingPageCount = 100
        else:
            trackingPageCount = 100
        
        listPageUrlList = []
        for categoryName in BT_DOWNLOAD_CATEGORY:
            categoryNumber = Category.categoryNameToNumberDict[categoryName]
            for trackingNumber in range(1, trackingPageCount + 1):
                url = "https://www.t66y.com/thread0806.php?fid={0}&search=&page={1}".format(str(categoryNumber),
                                                                                            str(trackingNumber))
                listPageUrlList.append(url)
        requestsList = []
        for listPageUrl in listPageUrlList:
            if COOKIES:
                requestsList.append(
                    AsyncRequests.get(listPageUrl, headers=self.headers, cookies=COOKIES)
                )
            else:
                requestsList.append(
                    AsyncRequests.get(listPageUrl, headers=self.headers)
                )
        resultList = AsyncRequests.map(requestsList, size=DOWNLOAD_CONCURRENT_COUNT)
        return resultList
    
    def getDetailsPageUrl(self, responseList):
        '''
        get details page url by list page
        input url to queue
        :return:
        '''
        if not responseList:
            logger.error("get response list is empty in details page function")
        detailsPageUrlList = []
        # get details page url from list page response
        try:
            for response in responseList:
                if response is not None and response.status_code == 200:
                    response.encoding = "gbk"
                    soup = bs(response.text, "lxml")
                    trList = soup.find_all("tr")
                    for tr in trList:
                        tdList = tr.find_all("td")
                        if len(tdList) == 5:
                            urlTagList = tdList[1].select('a[href]')
                            if urlTagList:
                                url = urlTagList[0]["href"]
                                # title = urlTagList[0].string
                                if url not in self.excludeUrlList:
                                    detailsPageUrlList.append(self.domains + url.strip())
            # url to response
            logger.info("get details page response ...")
            detailsPageResponseList = self.urlToResponse(detailsPageUrlList)
            logger.info("present craw count:{0}".format(str(len(detailsPageResponseList))))
            self.totalDownload = len(detailsPageResponseList)
            # put to queue
            for detailsPageResponse in detailsPageResponseList:
                self._taskQueue.put(detailsPageResponse)
        except BaseException:
            logger.error(traceback.format_exc())
    
    def getDownloadPageUrl(self, detailsResponse):
        '''
        get download page url by details page
        :param detailsResponse:
        :return:
        '''
        try:
            torrentResultClass = TorrentResultClass()
            if detailsResponse is not None and detailsResponse.status_code == 200:
                detailsResponse.encoding = "gbk"
                soup = bs(detailsResponse.text, "lxml")
                title = soup.head.title.text
                aTagList = soup.find_all("a")
                for a in aTagList:
                    downloadPageUrl = a.string
                    if downloadPageUrl:
                        if self.isDownloadPageUrl(downloadPageUrl):
                            torrentResultClass.setCategory(self.getCategoryFromDatailsPageUrl(str(detailsResponse.url)))
                            torrentResultClass.setCrawData(self.formatDate())
                            torrentResultClass.setDetailsPageUrl(str(detailsResponse.url))
                            torrentResultClass.setResponse(self.urlToResponse([downloadPageUrl.strip()])[0])
                            torrentResultClass.setTitle(self.clearTitle(title))
                    else:
                        continue
            # return self.getTorrentDownloadUrl(torrentResultClass)
            return torrentResultClass
        except BaseException:
            logger.error(traceback.format_exc())
            return None
    
    def getTorrentDownloadUrl(self, torrentResultClass):
        '''
        get torrent download url by download information page
        :param torrentResultClass:
        :return:
        '''
        if torrentResultClass is None:
            logger.error("get download page url failed, because torrentResultClass is None")
            return None
        try:
            response = torrentResultClass.getResponse()
            # i don't knonw why i might get a string here
            if isinstance(response, str):
                return None
            if response is not None and response.status_code == 200:
                response.encoding = "utf-8"
                downloadUrl = self.torrentDownloadUrl(response.text)
                torrentResultClass.setDownloadPageUrl(str(response.url))
                torrentResultClass.setTorrentDownloadUrl(downloadUrl)
                return torrentResultClass
            else:
                return None
        except BaseException:
            logger.error(traceback.format_exc())
            return None
    
    def downloadTorrentFile(self, torrentResultClass):
        '''
        download torrent file
        :param torrentResultClass:
        :return:
        '''
        if torrentResultClass is None:
            logger.error("torrentResultClass is None in the downloadTorrentFile function")
            return None
        torrentName = self.filterTorrentName(self.clearTitle(torrentResultClass.getTitle()))
        torrentDownloadUrl = torrentResultClass.getTorrentDownloadUrl()
        detailsPageUrl = torrentResultClass.getDetailsPageUrl()
        if not torrentName:
            logger.error("get torrent name failed")
            return None
        if not torrentDownloadUrl:
            logger.error("get torrent download url failed")
            return None
        if not detailsPageUrl:
            logger.error("get details page url failed")
            return None
        try:
            categoryName = self.getCategoryFromDatailsPageUrl(detailsPageUrl)
            torrentResponse = requests.get(torrentDownloadUrl, headers=self.headers)
            torrentMd5 = self.computeMD5ByFile(torrentResponse.content)
            # check save path is vailed
            torrentPath = self.checkDirExist(
                os.path.join(SAVE_PATH,
                             "torrent",
                             categoryName,
                             self.year(),
                             self.month(),
                             self.day(),
                             torrentName + ".torrent"))
            with open(torrentPath, "wb+") as file:
                file.write(torrentResponse.content)
            torrentResultClass.setSavePath(torrentPath)
            torrentResultClass.setCrawData(self.formatDate())
            torrentResultClass.setMd5(torrentMd5)
            torrentResultClass.setMagnet(self.torrentToMagnet(torrentResponse.content))
            torrentResultClass.setDownloaded(0)
            return torrentResultClass
        except BaseException:
            logger.error(traceback.format_exc())
            return None
    
    def torrentResultClassPreprocessing(self, torrentResultClass):
        '''
        the preprocessing torrentResultClass is used to write to the database
        :param torrentResultClass:
        :return:
        '''
        if torrentResultClass is None:
            logger.error("torrentResultClass is None in the torrentResultClassPreprocessign function")
            return None
        try:
            torrentResultDict = {}
            torrentResultDict.setdefault("id", None)
            torrentResultDict.setdefault("category", torrentResultClass.getCategory())
            torrentResultDict.setdefault("title", torrentResultClass.getTitle())
            torrentResultDict.setdefault("detailsPageUrl", torrentResultClass.getDetailsPageUrl())
            torrentResultDict.setdefault("downloadPageUrl", torrentResultClass.getDownloadPageUrl())
            torrentResultDict.setdefault("torrentDownloadUrl", torrentResultClass.getTorrentDownloadUrl())
            torrentResultDict.setdefault("savePath", torrentResultClass.getSavePath())
            torrentResultDict.setdefault("crawData", torrentResultClass.getCrawData())
            torrentResultDict.setdefault("md5", torrentResultClass.getMd5())
            torrentResultDict.setdefault("magnet", torrentResultClass.getMagnet())
            torrentResultDict.setdefault("downloaded", torrentResultClass.getDownloaded())
            return torrentResultDict
        except BaseException:
            logger.error(traceback.format_exc())
            return None
    
    def writeToDatabase(self, torrentResultDict):
        '''
        information write to database
        :param infoDict:
        :return:
        '''
        if torrentResultDict is None:
            logger.error("torrentResultDict is None")
            return None
        try:
            result = self._database.queryIsExist("torrent", {"md5": torrentResultDict["md5"]})
            progressBar = self.computeProgressBar(self.completed, self.totalDownload)
            if not result:
                
                logger.info("Torrent completed: {progressBar: <10}".format(progressBar=progressBar) + \
                            "category: {category: <20}".format(category=torrentResultDict['category']) + \
                            "Title:{title}".format(title=torrentResultDict['title']),
                            level="ALL")
                self._database.insert("torrent", torrentResultDict)
            else:
                logger.info("Torrent completed:{progressBar: <5} torrent already exist database.".format(
                    progressBar=progressBar))
        except BaseException:
            logger.error(traceback.format_exc())
            logger.error("An error occurred in the function ---> wirteToDataBase")
            return None
    
    def producer(self):
        '''
        used to produce details response
        :return:
        '''
        self._queueProducerStatus = True
        self.getDetailsPageUrl(self.generatorListPage())
        self._queueProducerStatus = False
    
    def consumer(self):
        '''
        used to consume details response
        get a response by queue, then get download page url by details page response,
        then get torrent download url by download page response
        :return:
        '''
        while not self._taskQueue.empty() or self._queueProducerStatus:
            # get detailsResponse
            detailsResponse = self._taskQueue.get()
            if detailsResponse is None:
                self.completed += 1
                continue
            # get download page url result is a torrentResultClass
            downloadPageUrlTorrentResultClass = self.getDownloadPageUrl(detailsResponse)
            if downloadPageUrlTorrentResultClass is None:
                self.completed += 1
                continue
            # get torrent download url result is a torrentResultClass
            torrentDownloadUrlTorrentResultClass = self.getTorrentDownloadUrl(downloadPageUrlTorrentResultClass)
            if torrentDownloadUrlTorrentResultClass is None:
                self.completed += 1
                continue
            # download torrent result is a torrentResultClass
            downloadTorrentFileTorrentResultClass = self.downloadTorrentFile(torrentDownloadUrlTorrentResultClass)
            if downloadTorrentFileTorrentResultClass is None:
                self.completed += 1
                continue
            # torrentResultClass to infoDict
            torrentResultDict = self.torrentResultClassPreprocessing(downloadTorrentFileTorrentResultClass)
            if torrentResultDict is None:
                self.completed += 1
                continue
            # infoDict write to database
            self.completed += 1
            self.writeToDatabase(torrentResultDict)


if __name__ == '__main__':
    # CodeTest.generatorListPage()
    # Scheduler.start()
    pass


