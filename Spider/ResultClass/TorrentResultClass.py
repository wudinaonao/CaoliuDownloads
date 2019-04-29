

class TorrentResultClass():
    
    _category = ""
    _title = ""
    _detailsPageUrl = ""
    _downloadPageUrl = ""
    _torrentDownloadUrl = ""
    _savePath = ""
    _resposne = ""
    _crawData = ""
    _md5 = ""
    _magnet = ""
    _downloaded = 0
    
    def getCategory(self):
        return self._category
    
    def setCategory(self, category):
        self._category = category
    
    def getTitle(self):
        return self._title
    
    def setTitle(self, title):
        self._title = title
    
    def getDetailsPageUrl(self):
        return self._detailsPageUrl
    
    def setDetailsPageUrl(self, detailsPageUrl):
        self._detailsPageUrl = detailsPageUrl
    
    def getDownloadPageUrl(self):
        return self._downloadPageUrl
    
    def setDownloadPageUrl(self, downloadPageUrl):
        self._downloadPageUrl = downloadPageUrl
    
    def getTorrentDownloadUrl(self):
        return self._torrentDownloadUrl
    
    def setTorrentDownloadUrl(self, torrentDownloadUrl):
        self._torrentDownloadUrl = torrentDownloadUrl
    
    def getSavePath(self):
        return self._savePath
    
    def setSavePath(self, savePath):
        self._savePath = savePath
    
    def getResponse(self):
        return self._resposne
    
    def setResponse(self, response):
        self._resposne = response
    
    def getCrawData(self):
        return self._crawData
    
    def setCrawData(self, crawData):
        self._crawData = crawData
    
    def getMd5(self):
        return self._md5
    
    def setMd5(self, md5):
        self._md5 = md5
    
    def getMagnet(self):
        return self._magnet
    
    def setMagnet(self, magnet):
        self._magnet = magnet
    
    def getDownloaded(self):
        return self._downloaded
    
    def setDownloaded(self, downloaded):
        self._downloaded = downloaded