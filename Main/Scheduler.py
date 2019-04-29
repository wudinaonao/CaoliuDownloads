from queue import Queue
from Spider.Video import Video
from Spider.Torrent import Torrent
from Spider.Image import Image
import threading
from Config.Config import DOWNLOAD_CONCURRENT_COUNT
from Tools.Log import Log as logger

class Scheduler():
    
    @classmethod
    def start(cls):
        cls.downloadImage()
        cls.downloadTorrent()
        # cls.downloadVideo()
        
    @classmethod
    def downloadTorrent(cls):
        logger.info("start download torrent")
        taskQueue = Queue(maxsize=128)
        torrentSpider = Torrent(taskQueue)
        threading.Thread(target=torrentSpider.producer, name="producer").start()
        for i in range(DOWNLOAD_CONCURRENT_COUNT):
            threading.Thread(target=torrentSpider.consumer, name="ThreadID:{0}".format(str(i))).start()
            # task = threading.Thread(target=videoSpider.consumer, name="ThreadID:{0}".format(str(i)))
    
    @classmethod
    def downloadImage(cls):
        logger.info("start download image")
        taskQueue = Queue(maxsize=128)
        imageSpider = Image(taskQueue)
        threading.Thread(target=imageSpider.producer, name="producer").start()
        for i in range(DOWNLOAD_CONCURRENT_COUNT * 2):
            threading.Thread(target=imageSpider.consumer, name="ThreadID:{0}".format(str(i))).start()
            # task = threading.Thread(target=imageSpider.consumer, name="ThreadID:{0}".format(str(i)))
    
    @classmethod
    def downloadVideo(cls):
        logger.info("start download video")
        downloadVideo = Video()
        threading.Thread(target=downloadVideo.downloadScheduler, name="downloadVideo").start()
    
if __name__ == '__main__':
    
    Scheduler.start()