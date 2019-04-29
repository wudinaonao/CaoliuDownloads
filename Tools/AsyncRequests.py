from requests_futures.sessions import FuturesSession
import time
import traceback
import requests
from Tools.Log import Log as logger

class AsyncRequests():
    
    '''
    Simple packaging async requests
    How to use it by reference to grequests
    '''
    @classmethod
    def get(self, url, params=None, **kwargs):
        return {"method":"get",
                "url": url,
                "params": params,
                "other": kwargs}
    
    @classmethod
    def post(self, url, data=None, json=None, **kwargs):
        return {"method":"post",
                "url": url,
                "data": data,
                "json": json,
                "other": kwargs}
    
    @classmethod
    def map(self, requestArgsList, size=256, gtimeout=60):
        requestsList = []
        resultList = []
        with FuturesSession(max_workers=size) as session:
            for requestArgs in requestArgsList:
                if requestArgs['method'] == "get":
                    request = session.get(url=requestArgs['url'],
                                          params=requestArgs['params'],
                                          **requestArgs['other'])
                elif requestArgs['method'] == "post":
                    request = session.post(url=requestArgs['url'],
                                           data=requestArgs['data'],
                                           json=requestArgs['json'],
                                           **requestArgs['other'])
                else:
                    request = None
                requestsList.append(request)

            
            for result in requestsList:
                try:
                    result = result.result()
                except requests.exceptions.ConnectTimeout:
                    result = None
                except BaseException:
                    # logger.error(traceback.format_exc())
                    result = None
                resultList.append(result)
        return resultList

    @classmethod
    def _checkTimeOut(cls, startTime, timeOut):
        if time.time() - startTime > timeOut:
            return True
        return False

if __name__ == '__main__':
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
    }
    
    url = "https://www.baidu.com"
    t1 = time.time()
    requestList = [AsyncRequests.get(url, headers=headers, timeout=10) for _ in range(1000)]
    AsyncRequests.map(requestList)
    print("Time: {0}".format(str(time.time() - t1)))
