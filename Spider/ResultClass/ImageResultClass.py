
class ImageResultClass():

    _title = ""
    _detailsPageUrl = ""
    _detailsPageImageCount = ""
    _imageDownloadUrl = ""
    _savePath = ""
    _response = ""
    _crawData = ""
    _md5 = ""
    
    def getTitle(self):
        return self._title
    
    def setTitle(self, title):
        self._title = title
        
    def getDetailsPageUrl(self):
        return self._detailsPageUrl
    
    def setDetailsPageUrl(self, detailsPageUrl):
        self._detailsPageUrl = detailsPageUrl
        
    def getDetailsPageImageCount(self):
        return self._detailsPageImageCount
    
    def setDetailsPageImageCount(self, detailsPageImageCount):
        self._detailsPageImageCount = detailsPageImageCount
        
    def getImageDownloadUrl(self):
        return self._imageDownloadUrl
    
    def setImageDownloadUrl(self, imageDownloadUrl):
        self._imageDownloadUrl = imageDownloadUrl
    
    def getSavePath(self):
        return self._savePath
    
    def setSavePath(self, savePath):
        self._savePath = savePath
        
    def getResponse(self):
        return self._response
    
    def setResponse(self, response):
        self._response = response
        
    def getCrawDate(self):
        return self._crawData
    
    def setCrawDate(self, crawDate):
        self._crawData = crawDate
    
    def getMd5(self):
        return self._md5
    
    def setMd5(self, md5):
        self._md5 = md5
        
    
