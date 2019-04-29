import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])

from Config.Config import TRACKING_PAGE_COUNT
from Config.Config import DOWNLOAD_CONCURRENT_COUNT
from Config.Config import COOKIES
from Config.Config import SAVE_PATH
from Spider.ResultClass.ImageResultClass import ImageResultClass
from Tools.AsyncRequests import AsyncRequests
from bs4 import BeautifulSoup as bs
from Tools.Log import Log as logger
import traceback
from Tools.GeneralTool import GeneralTool
from DataBase.DBUtil import DBUtil

class Image(GeneralTool):
    
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
        for trackingNumber in range(1, trackingPageCount + 1):
            url = "https://www.t66y.com/thread0806.php?fid=16&search=&page={0}".format(str(trackingNumber))
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
                                if url not in self.excludeUrlList and not self.urlInExclued(url):
                                    detailsPageUrlList.append(self.domains + url.strip())
            # url to response
            logger.info("get details page response ...")
            detailsPageResponseList = self.urlToResponse(detailsPageUrlList)
            self.totalDownload = len(detailsPageResponseList)
            logger.info("present craw count:{0}".format(str(len(detailsPageResponseList))))
            # put to queue
            for detailsPageResponse in detailsPageResponseList:
                self._taskQueue.put(detailsPageResponse)
        except BaseException:
            logger.error(traceback.format_exc())
            
    def computeDetailsImageCount(self, detailsResponse):
        '''
        compute details image count bt detailsResponse
        :param detailsResponse:
        :return:
        '''
        try:
            if detailsResponse is not None and detailsResponse.status_code == 200:
                detailsResponse.encoding = "gbk"
                soup = bs(detailsResponse.text, "lxml")
                inputTagList = soup.find_all("input")
                imageCount = 0
                for inputTag in inputTagList:
                    try:
                        imageDownloadUrl = inputTag['data-src']
                        imageCount += 1
                    except KeyError:
                        continue
                return imageCount
            else:
                logger.error("detalisResponse is None or status code not 200 in the computeDetailsImageCount function")
                return 0
        except BaseException:
            logger.error(traceback.format_exc())
            return 0
        
    def getImageDownloadUrlGenerator(self, detailsResponse):
        '''
        get download page url by details page
        this is a generator function
        generator imageResultClass
        :param detailsResponse:
        :return: imageResultClassList
        '''
        try:
            # imageResultClassList = []
            if detailsResponse is not None and detailsResponse.status_code == 200:
                detailsResponse.encoding = "gbk"
                soup = bs(detailsResponse.text, "lxml")
                title = soup.head.title.text
                inputTagList = soup.find_all("input")
                for inputTag in inputTagList:
                    try:
                        imageDownloadUrl = inputTag['data-src']
                    except KeyError:
                        continue
                    if imageDownloadUrl:
                        # print("is ok")
                        if self.existInDatabase("image", {"imageDownloadUrl": imageDownloadUrl}):
                            continue
                        if self.isImageDownloadPageUrl(imageDownloadUrl):
                            # imageResultClass.setCategory(self.getCategoryFromDatailsPageUrl(str(detailsResponse.url)))
                            imageResultClass = ImageResultClass()
                            imageResultClass.setCrawDate(self.formatDate())
                            imageResultClass.setDetailsPageUrl(str(detailsResponse.url))
                            imageResultClass.setDetailsPageImageCount(str(self.computeDetailsImageCount(detailsResponse)))
                            imageResultClass.setImageDownloadUrl(imageDownloadUrl)
                            imageResultClass.setResponse(self.urlToResponse([imageDownloadUrl])[0])
                            imageResultClass.setTitle(self.clearTitle(title))
                            imageResultClass.setCrawDate(self.formatDate())
                            yield imageResultClass
                            # imageResultClassList.append(imageResultClass)
                    else:
                        continue
            # return imageResultClassList
        except BaseException:
            logger.error(traceback.format_exc())
            return None
      
    def saveImageGenerator(self, imageResultClassGenerator):
        '''
        save image by image result class list
        :param imageResultClassList:
        :return:
        '''
        if imageResultClassGenerator is None:
            logger.error("imageResultClass generator is None")
            return None
        for imageResultClass in imageResultClassGenerator:
            try:
                # imageResultClass = imageResultClassGenerator.__next__()
                if isinstance(imageResultClass, str):
                    continue
                response = imageResultClass.getResponse()
                if response is not None and response.status_code == 200:
                    imageByte = imageResultClass.getResponse().content
                    imageMd5 = self.computeMD5ByFile(imageByte)
                    imageResultClass.setMd5(imageMd5)
                    imageName = os.path.split(imageResultClass.getImageDownloadUrl())[1]
                    imageDirName = imageResultClass.getTitle()
                    # check save path is vailed
                    imageSavePath = self.checkDirExist(os.path.join(SAVE_PATH,
                                                                    "image",
                                                                    self.year(),
                                                                    self.month(),
                                                                    self.day(),
                                                                    imageDirName,
                                                                    imageName))
                    imageResultClass.setSavePath(imageSavePath)
                    with open(imageSavePath, "wb+") as fo:
                        fo.write(imageByte)
                    yield imageResultClass
            # except StopIteration:
            #     break
            except BaseException:
                logger.error(traceback.format_exc())
                return None
        # return imageResultClassList
    
    # def imageResultClassListGenerator(self, imageResultClassList):
    
    
    def imageResultClassPreprocessing(self, imageResultClass):
        '''
        the preprocessing infoClass is used to write to the database
        :param infoClass:
        :return:
        '''
        if imageResultClass is None:
            logger.error("imageResultClass is None in the imageResultClassPreprocessign function")
            return None
        try:
            
            imageResultDict = {}
            imageResultDict.setdefault("id", None)
            imageResultDict.setdefault("title", imageResultClass.getTitle())
            imageResultDict.setdefault("detailsPageUrl", imageResultClass.getDetailsPageUrl())
            imageResultDict.setdefault("detailsPageImageCount", imageResultClass.getDetailsPageImageCount())
            imageResultDict.setdefault("imageDownloadUrl", imageResultClass.getImageDownloadUrl())
            imageResultDict.setdefault("savePath", imageResultClass.getSavePath())
            imageResultDict.setdefault("crawData", imageResultClass.getCrawDate())
            imageResultDict.setdefault("md5", imageResultClass.getMd5())
            return imageResultDict
        except BaseException:
            logger.error(traceback.format_exc())
            return None
    
    def writeToDatabase(self, imageResultDict):
        '''
        information write to database
        :param infoDict:
        :return:
        '''
        if imageResultDict is None:
            logger.error("imageResultDict is None")
            return None
        try:
            result = self._database.queryIsExist("image", {"md5": imageResultDict["md5"]})
            progressBar = self.computeProgressBar(self.completed, self.totalDownload)
            if not result:
                logger.info("Image completed: {progressBar: <10}".format(progressBar=progressBar) + \
                            "Title:{title}".format(title=imageResultDict['title']),
                            level="ALL")
                self._database.insert("image", imageResultDict)
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
        get a details page response by queue, then get image download url by details page response,
        then save image to local dir, then write to database
        :return:
        '''
        while not self._taskQueue.empty() or self._queueProducerStatus:
            # get detailsResponse
            detailsResponse = self._taskQueue.get()
            if detailsResponse is None:
                continue
            # get image download url result is a imageResultClass generator
            imageDownloadUrlGenerator = self.getImageDownloadUrlGenerator(detailsResponse)
            if imageDownloadUrlGenerator is None:
                continue
            # save image to dir result is a imageResultClass
            imageResultClassGenerator = self.saveImageGenerator(imageDownloadUrlGenerator)
            for imageResultClass in imageResultClassGenerator:
                if imageResultClass is None:
                    continue
                # imageResultClass to imageResultDict
                imageResultDict = self.imageResultClassPreprocessing(imageResultClass)
                if imageResultDict is None:
                    continue
                # imageResultDict write to database
                self.writeToDatabase(imageResultDict)
            self.completed += 1
            progressBar = self.computeProgressBar(self.completed, self.totalDownload)
            logger.info("Image completed:{0}".format(progressBar))

            
if __name__ == '__main__':
    
    pass