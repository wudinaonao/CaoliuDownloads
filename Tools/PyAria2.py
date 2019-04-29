'''
Author: wudinaonao
e-mail:wudinaonao250@gmail.com

通过python调用aria2下载,通过rpc实现
示例:
pyaria2 = Pyaria2("主机地址", "端口",)
pyaria2.addUrls("下载地址")
'''
import json
import requests
import hashlib
import random
import base64

class PyAria2(object):

    def __init__(self, host, port, token=None, link_type="http"):
        self.host = host
        self.port = port
        self.token = token
        self.link_type = link_type
        self.ServerUrl = "{link_type}://{host}:{port}/jsonrpc".format(link_type=link_type, host=host, port=port)

    def _get_id(self):
        '''
        取一个随机值进行md5编码得到一个id号
        :return: id号
        '''
        raw_str = str(int(random.randint(0, 100000)))
        raw_str += "wudinaonao"
        raw_str = raw_str.encode('utf-8')
        md5 = hashlib.md5()
        md5.update(raw_str)
        return md5.hexdigest()

    def _getResult(self, reqName, token, active=None, url=None, postion=None, gid=None, key=None,value=None):
        if token:
            req = {
                "jsonrpc": "2.0",
                "method": str(reqName),
                "id": str(self._get_id()),
                "params": [
                    "token:" + str(self.token),
                ]
            }
            if active:
                req = {
                    "jsonrpc": "2.0",
                    "method": str(reqName),
                    "id": str(self._get_id()),
                    "params": [
                        "token:" + str(self.token),
                        [
                            "gid",
                            "totalLength",
                            "completedLength",
                            "uploadSpeed",
                            "downloadSpeed",
                            "connections",
                            "numSeeders",
                            "seeder",
                            "status",
                            "errorCode"
                        ]
                    ]
                }
            if url:
                req = {
                    "jsonrpc": "2.0",
                    "method": str(reqName),
                    "id": str(self._get_id()),
                    "params": [
                        "token:" + str(self.token),
                            [url],
                            {}
                    ]
                }
                if postion:
                    req = {
                        "jsonrpc": "2.0",
                        "method": str(reqName),
                        "id": str(self._get_id()),
                        "params": [
                            "token:" + str(self.token),
                                [url],
                                postion
                        ]
                    }
            if gid:
                req = {
                    "jsonrpc": "2.0",
                    "method": str(reqName),
                    "id": str(self._get_id()),
                    "params": [
                        "token:" + str(self.token), [gid]
                    ]
                }
            if key and value:
                req = {
                    "jsonrpc": "2.0",
                    "method": str(reqName),
                    "id": str(self._get_id()),
                    "params": [
                        "token:" + str(self.token),
                        {
                            key: value
                        }
                    ]
                }
        else:
            req = {
                "jsonrpc": "2.0",
                "method": str(reqName),
                "id": str(self._get_id()),
                "params": []
            }
            if active:
                req = {
                    "jsonrpc": "2.0",
                    "method": str(reqName),
                    "id": str(self._get_id()),
                    "params": [
                        [
                            "gid",
                            "totalLength",
                            "completedLength",
                            "uploadSpeed",
                            "downloadSpeed",
                            "connections",
                            "numSeeders",
                            "seeder",
                            "status",
                            "errorCode"
                        ]
                    ]
                }
            if url:
                req = {
                    "jsonrpc": "2.0",
                    "method": str(reqName),
                    "id": str(self._get_id()),
                    "params": [
                            [url],
                            {}
                    ]
                }
                if postion:
                    req = {
                        "jsonrpc": "2.0",
                        "method": str(reqName),
                        "id": str(self._get_id()),
                        "params": [
                                [url],
                                postion
                        ]
                    }
            if gid:
                req = {
                    "jsonrpc": "2.0",
                    "method": str(reqName),
                    "id": str(self._get_id()),
                    "params": [gid]
                }
            if key and value:
                req = {
                    "jsonrpc": "2.0",
                    "method": str(reqName),
                    "id": str(self._get_id()),
                    "params": [
                        {
                            key: value
                        }
                    ]
                }
        results = requests.post(url=self.ServerUrl, data=json.dumps(req))
        results.encoding = 'utf-8'
        res_json = json.loads(results.text)
        if 'result' in res_json:
            return res_json['result']
        else:
            return res_json['error']

    def getGlobalStat(self):
        '''
        获取全局状态
        :return:
        '''
        reqName = "aria2.getGlobalStat"
        info_dict = self._getResult(reqName=reqName, token=self.token)
        if len(str(info_dict['downloadSpeed'])) > 3:
            info_dict['downloadSpeed'] = str(round(int(info_dict['downloadSpeed']) / 1024, 2)) + "KB/s"
        elif len(str(info_dict['downloadSpeed'])) > 6:
            info_dict['downloadSpeed'] = str(round(int(info_dict['downloadSpeed']) / 102400, 2)) + "MB/s"
        else:
            info_dict['downloadSpeed'] = str(round(int(info_dict['downloadSpeed']), 2)) + "k/s"
        if len(str(info_dict['uploadSpeed'])) > 3:
            info_dict['uploadSpeed'] = str(round(int(info_dict['uploadSpeed']) / 1024, 2)) + "KB/s"
        elif len(str(info_dict['uploadSpeed'])) > 6:
            info_dict['uploadSpeed'] = str(round(int(info_dict['uploadSpeed']) / 102400, 2)) + "MB/s"
        else:
            info_dict['uploadSpeed'] = str(round(int(info_dict['uploadSpeed']), 2)) + "k/s"
        return info_dict

    def tellActive(self):
        '''
        查询活动任务的信息, 例如下载速度,GID
        :return:
        '''
        reqName = "aria2.tellActive"
        return self._getResult(reqName=reqName, token=self.token, active=True)

    def tellStatus(self, gid):
        '''
        获取任务状态
        :param gid: 任务GID
        :return:
        '''
        reqName = "aria2.tellStatus"
        return self._getResult(reqName=reqName, token=self.token, gid=gid)

        # 返回值
        # {u'id': u'qwer',
        #  u'jsonrpc': u'2.0',
        #  u'result': {u'bitfield': u'0000000000',
        #              u'completedLength': u'901120',
        #              u'connections': u'1',
        #              u'dir': u'/downloads',
        #              u'downloadSpeed': u'15158',
        #              u'files': [{u'index': u'1',
        #                          u'length': u'34896138',
        #                          u'completedLength': u'34896138',
        #                          u'path': u'/downloads/file',
        #                          u'selected': u'true',
        #                          u'uris': [{u'status': u'used',
        #                                     u'uri': u'http://example.org/file'}]}],
        #              u'gid': u'2089b05ecca3d829',
        #              u'numPieces': u'34',
        #              u'pieceLength': u'1048576',
        #              u'status': u'active',
        #              u'totalLength': u'34896138',
        #              u'uploadLength': u'0',
        #              u'uploadSpeed': u'0'}}

    def addUrls(self, url, postion=None):
        '''
        增加下载任务
        :param url:下载地址
        :param postion: 存储位置
        :return: 任务GID
        '''
        postion_dict = {}
        if postion is not None:
            postion_dict.setdefault("dir", postion)
        reqName = "aria2.addUri"
        # 返回任务GID
        return self._getResult(reqName=reqName, token=self.token, url=url, postion=postion_dict)

    def addTorrent(self, torrentPath, postion=None):
        '''
        添加种子任务
        :param torrentPath: 种子路径,绝对地址
        :param postion: 存放目录
        :return:
        '''
        postion_dict = {}
        if postion is not None:
            postion_dict.setdefault("dir", postion)
        torrent = base64.b64encode(open(torrentPath, "rb").read())
        reqName = "aria2.addTorrent"
        # 返回任务GID
        return self._getResult(reqName=reqName, token=self.token, url=torrent, postion=postion_dict)

    def addMetalink(self, metalinkPath, postion=None):
        '''
        添加Metalink任务
        :param metalinkPath: Metalink文件路径, 绝对路径
        :param postion: 存储目录 string
        :return:
        '''
        postion_dict = {}
        if postion is not None:
            postion_dict.setdefault("dir", postion)
        metalink = base64.b64encode(open(metalinkPath).read())
        reqName = "aria2.addMetalink"
        # 返回任务GID
        return self._getResult(reqName=reqName, token=self.token, url=metalink, postion=postion_dict)

    def reMove(self, gid):
        '''
        删除任务
        :param gid:任务GID
        :return:
        '''
        reqName = "aria2.remove"
        return self._getResult(reqName=reqName, token=self.token, gid=gid)

    def clearFinish(self):
        '''
        清空已完成任务
        :return:
        '''
        reqName = "aria2.purgeDownloadResult"
        return self._getResult(reqName=reqName, token=self.token)

    def changeGlobalOption(self, key, value):
        '''
        改变配置
        :param key: 配置名称
        :param value: 值
        :return:
        '''
        reqName = "aria2.changeGlobalOption"
        return self._getResult(reqName=reqName, token=self.token, key=key, value=value)



