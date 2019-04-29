from DataBase.DBUtil import DBUtil
from Tools.Log import Log as logger

class FirstRun():

    _database = DBUtil()
    
    @classmethod
    def imageTableSQL(cls):
        sql = "CREATE TABLE `image` (" + \
            "  `id` bigint(20) NOT NULL AUTO_INCREMENT," + \
            "  `title` varchar(255) NOT NULL," + \
            "  `detailsPageUrl` varchar(255) NOT NULL," + \
            "  `detailsPageImageCount` varchar(255) NOT NULL," + \
            "  `imageDownloadUrl` varchar(255) NOT NULL," + \
            "  `savePath` varchar(255) NOT NULL," + \
            "  `crawData` varchar(255) NOT NULL," + \
            "  `md5` char(32) NOT NULL," + \
            "  PRIMARY KEY (`id`), " + \
            "  UNIQUE KEY `md5` (`md5`)" + \
            ") ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;"
        return sql
    
    @classmethod
    def torrentTableSQL(cls):
        sql = "CREATE TABLE `torrent` (" + \
            "  `id` bigint(20) NOT NULL AUTO_INCREMENT," + \
            "  `category` varchar(255) NOT NULL," + \
            "  `title` varchar(255) NOT NULL," + \
            "  `detailsPageUrl` varchar(255) NOT NULL," + \
            "  `downloadPageUrl` varchar(255) NOT NULL," + \
            "  `torrentDownloadUrl` varchar(255) NOT NULL," + \
            "  `savePath` varchar(255) DEFAULT NULL," + \
            "  `crawData` varchar(255) NOT NULL," + \
            "  `md5` char(32) NOT NULL," + \
            "  `magnet` varchar(255) NOT NULL," + \
            "  `downloaded` char(1) NOT NULL," + \
            "  PRIMARY KEY (`id`)," + \
            "  UNIQUE KEY `md5` (`md5`)" + \
            ") ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;"
        return sql
    
    @classmethod
    def createTable(cls):
        # create image table
        if not cls._database.executeCustomSQL(cls.imageTableSQL()):
            logger.error("create image table failed")
            return None
        if not cls._database.executeCustomSQL(cls.torrentTableSQL()):
            logger.error("create torrent table failed")
            return None
        logger.info("create table image and torrent success")
    
if __name__ == '__main__':
    
    FirstRun.createTable()
